import asyncio

global_dict = {}


def handle_set(key, value, *extra_args):
    if extra_args:
        response = b'-ERR wrong number of args'
    else:
        global_dict[key] = value
        response = b'+OK\r\n'
    return response


def handle_get(key, *extra_args):
    if extra_args:
        response = b'-ERR wrong number of args'
    else:
        val = global_dict.get(key)
        if val:
            response = f"${len(val)}\r\n{val}\r\n".encode()
        else:
            response = b'$-1\r\n'
    return response


def encode_bulk_string(values):
    encoded_vals = []

    for val in values:
        encoded_value = f"${len(val)}\r\n{val}\r\n".encode()
        encoded_vals.append(encoded_value)
    return b"".join(encoded_vals)


async def read_resp_array(header, reader):
    num_items = int(header[1:])

    array = []
    for i in range(num_items):
        item_header = await reader.readline()
        item_size = int(item_header[1:])
        item_data = await reader.readexactly(item_size + 2)
        item = item_data[:-2].decode()
        array.append(item)
    return array


async def handle_clients(reader, writer):
    while True:
        try:
            command = await reader.readline()
            if not command:
                break

            if command[0] == ord(b'*'):
                array = await read_resp_array(command, reader)

            if array[0].lower() == "ping":
                writer.write(b"+PONG\r\n")
                await writer.drain()
            elif array[0].lower() == "echo":
                response = encode_bulk_string(array[1:])
                writer.write(response)
                await writer.drain()
            elif array[0].lower() == "get":
                response = handle_get(array[1])
                writer.write(response)
                await writer.drain()
            elif array[0].lower() == "set":
                response = handle_set(array[1], array[2])
                writer.write(response)
                await writer.drain()

        except Exception as e:
            print(command)
            print(f"Error in handling client: {e}")

    writer.close()


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
