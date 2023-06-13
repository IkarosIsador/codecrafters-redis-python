import asyncio


async def handle_clients(reader, writer):
    while True:
        reader.read(1024)
        writer.write(b"+PONG\r\n")
        await writer.drain()


async def start_server():
    server = await asyncio.start_server(handle_clients, "localhost", 6379)
    addr = server.sockets[0].getsockname()
    print(f'serving on {addr}')

    async with server:
        await server.serve_forever()


async def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    await start_server()


if __name__ == "__main__":
    asyncio.run(main())
