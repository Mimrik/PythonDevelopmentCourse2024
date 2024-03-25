import cmd
import threading
import readline
import socket
from typing import NoReturn

import select


lock = threading.Lock()


class NetcatCowClient(cmd.Cmd):
    @staticmethod
    def do_login(args) -> None:
        """Login by cow name"""
        s.send(f"login {args}\n".encode())

    @staticmethod
    def complete_login(pfx):
        with lock:
            s.send("cows\n".encode())
            msg = recv().strip().split(': ')[1]
            cows = msg.split(', ')
            return [s for s in cows if s.startswith(pfx)]

    @staticmethod
    def do_who(_) -> None:
        """List of active cows on server"""
        s.send("who\n".encode())

    @staticmethod
    def do_cows(_) -> None:
        """list of available cows on server"""
        s.send("cows\n".encode())

    @staticmethod
    def do_yield(args):
        """Send message to all users"""
        s.send(f"yield {args}\n".encode())

    @staticmethod
    def do_say(args) -> None:
        """Send message user"""
        s.send(f"say {args}\n".encode())

    @staticmethod
    def complete_say(pfx) -> list[str]:
        with lock:
            if len(pfx.split()) <= 1:
                s.send("who\n".encode())
                msg = recv().strip().split(": ")[1]
                users = msg.split(", ")
                return [s for s in users if s.startswith(pfx)]

    @staticmethod
    def do_exit(_) -> int:
        """Exit from netcat cow client"""
        s.send("exit\n".encode())
        return 1


def recv(timeout=0.0) -> str:
    readable, _, _ = select.select([s], [], [], timeout)
    for soc in readable:
        msg = soc.recv(1024).decode()
        return msg


def messenger(cmdline) -> NoReturn:
    try:
        while True:
            with lock:
                msg = recv()
            if msg:
                print(f"\n{msg.strip()}")
                print(f"{cmdline.prompt}{readline.get_line_buffer()}", end="", flush=True)
    except ValueError:
        print("Error: session closed")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("0.0.0.0", 1337))
    s.setblocking(False)
    netcat_cow_client = NetcatCowClient()
    chat = threading.Thread(target=messenger, args=(netcat_cow_client,))
    chat.start()
    netcat_cow_client.cmdloop()
