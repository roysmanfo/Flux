from ...helpers.commands import *
from ...helpers.arguments import Parser

import socket
from threading import Thread, Event

ENTRY_POINT = "Netcat"

class Netcat(CommandInterface):
    def init(self):
        self.parser = Parser("netcat", description="arbitrary TCP and UDP connections and listens")
        self.parser.add_argument("destination", nargs="?")
        self.parser.add_argument("port", nargs="?")
        self.parser.add_argument("-l", action="store_true", help="Listen mode, for inbound connects")

    def setup(self):
        super().setup()

        if self.status == STATUS_ERR:
            return
        
        if self.args.l:
            self.args.port = self.args.destination


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.args.port = int(self.args.port)
            sock.connect((self.args.destination, self.args.port))
            event = Event()
            Thread(target=self.recv_messages, args=(sock, event), daemon=True).start()

            try:
                while not event.is_set():
                    msg = self.input()
                    if msg:
                        sock.send(msg.encode())
                    else:
                        event.set()

            except (KeyboardInterrupt, ConnectionAbortedError):
                pass
            finally:
                event.set()

    def recv_messages(self, sock: socket.socket, event: Event) -> None:
        try:
            while not event.is_set():
                recv = sock.recv(4096)
                if recv:
                    self.print(recv.decode(), end="")
                else:
                    event.set()
        except (KeyboardInterrupt, ConnectionAbortedError):
            pass
        finally:
            event.set()
