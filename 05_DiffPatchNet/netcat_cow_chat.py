import asyncio
from cowsay import list_cows, cowsay

cow_set = set(list_cows())
client_to_queue = {}


async def who_process(writer) -> None:
    writer.write(f"Active cows: \n{', '.join(client_to_queue.keys())}\n".encode())
    await writer.drain()


async def cows_process(writer) -> None:
    writer.write(f"Available cows: {', '.join(cow_set)}\n".encode())


async def login_process(is_active, writer, input_line, receive) -> tuple[bool, str]:
    me = None
    if not is_active:
        if len(input_line) < 2:
            writer.write("No argument for login\n".encode())
            await writer.drain()
        else:
            me = input_line[1]
            if me in cow_set:
                cow_set.remove(me)
                client_to_queue[me] = asyncio.Queue()
                is_active = True
                print(f"Welcome to server, {me}!")

                for out in client_to_queue.values():
                    if out is not client_to_queue[me]:
                        await out.put(f"{me} is here")
                writer.write(f"Registered as {me}\n".encode())
                await writer.drain()

                receive.cancel()
                asyncio.create_task(client_to_queue[me].get())
            else:
                writer.write("That cow is unavailable\n".encode())
                await writer.drain()
    else:
        writer.write(f"You already registered".encode())
        await writer.drain()

    return is_active, me


async def say_process(is_active, writer, input_line, me) -> None:
    if not is_active:
        writer.write("Login first!\n".encode())
        await writer.drain()
    else:
        if len(input_line) < 3:
            writer.write("No arguments for say\n".encode())
            await writer.drain()
        else:
            receiver = input_line[1]
            message = " ".join(input_line[2:])
            await client_to_queue[receiver].put(f"{me} whispers:\n{cowsay(message, cow=me)}")
            writer.write(f"{me} whispers:\n{cowsay(message, cow=me)}\n".encode())
            await writer.drain()


async def yield_process(is_active, writer, input_line, me) -> None:
    if not is_active:
        writer.write("Login first!\n".encode())
        await writer.drain()
    else:
        if len(input_line) < 2:
            writer.write("No argument for yield\n".encode())
            await writer.drain()
        else:
            message = " ".join(input_line[1:])
            for out in client_to_queue.values():
                if out is not client_to_queue[me]:
                    await out.put(f"{me} says:\n{cowsay(message, cow=me)}")
            writer.write(f"{me} says:\n{cowsay(message, cow=me)}\n".encode())
            await writer.drain()


async def quit_process(me) -> None:
    for out in client_to_queue.values():
        if out is not client_to_queue[me]:
            await out.put(f"{me} leaves")


async def cow_chat(reader, writer):
    is_quit = False
    is_active = False

    send_list = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(asyncio.Queue().get())

    while not reader.at_eof() and not is_quit:
        done_list, pending = await asyncio.wait([send_list, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done_list:
            if q is send_list:
                send_list = asyncio.create_task(reader.readline())
                input_line = q.result().decode().strip().split()
                if len(input_line) == 0:
                    continue
                command = input_line[0]

                if command == "who":
                    await who_process(writer)

                elif command == "cows":
                    await cows_process(writer)

                elif command == "login":
                    is_active, me = await login_process(is_active, writer, input_line, receive)

                elif command == "say":
                    await say_process(is_active, writer, input_line, me)

                elif command == "yield":
                    await say_process(is_active, writer, input_line, me)

                elif command == "quit":
                    await quit_process(me)
                    is_quit = True
                    break
                else:
                    continue
            elif q is receive:
                receive = asyncio.create_task(client_to_queue[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    send_list.cancel()
    receive.cancel()
    del client_to_queue[me]
    cow_set.add(me)
    writer.close()
    await writer.wait_closed()


async def main() -> None:
    server = await asyncio.start_server(cow_chat, "0.0.0.0", 1337)
    async with server:
        await server.serve_forever()


asyncio.run(main())
