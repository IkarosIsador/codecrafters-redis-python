import asyncio


async def handle_clients(reader, writer):
    try:
        while True:
            data = await reader.read(256)
            if not data:
                break

            print(b'+PONG\r\n')
            writer.write(b'+PONG\r\n')
            await writer.drain()

    except Exception as e:
        print(f"Error in handling client: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def start_server():
    server = await asyncio.start_server(handle_clients, "localhost", 6379)
    addr = server.sockets[0].getsockname()
    print(f'serving on {addr}')

    async with server:
        await server.serve_forever()


async def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests
    await start_server()


if __name__ == "__main__":
    asyncio.run(main())
