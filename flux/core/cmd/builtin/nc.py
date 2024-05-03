from ...helpers.commands import *
from ...helpers.arguments import Parser

import socket
from threading import Thread, Event

ENTRY_POINT = "Netcat"

class Netcat(CommandInterface):
    def init(self):
        self.parser = Parser("nc", description="arbitrary TCP and UDP connections and listens")
        self.parser.add_argument("destination", nargs="?")
        self.parser.add_argument("port", nargs="?")
        self.parser.add_argument("-l", action="store_true", help="Listen mode, for inbound connects")
        self.parser.add_argument("-p", dest="PORT", help="Specify local port for remote connects")

    def setup(self):
        super().setup()

        if self.status == STATUS_ERR:
            return
        
        if self.args.l:
            if not self.args.PORT:
                self.error("missing port number")
                return

            self.args.port = self.args.PORT
            

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            self.args.port = int(self.args.port)
            event = Event()


            if self.args.l:
                self.host_as_server(sock)
            else:
                sock.connect((self.args.destination, self.args.port))
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

    def host_as_server(self, sock: socket.socket) -> None:
        event = Event()
        sock.bind(("0.0.0.0", self.args.port))
        sock.listen(5)

        self.print(f"Listening on 0.0.0.0 {self.args.port}")
        client, addr = sock.accept()
        self.print(f"Connection received on {addr[0]} {addr[1]}")
        Thread(target=self.recv_messages, args=(client, event), daemon=True).start()
        self.send_messages(client, event)

    def host_as_client(self, sock: socket.socket) -> None:
        event = Event()

        sock.connect((self.args.destination, self.args.port))
        Thread(target=self.recv_messages, args=(sock, event), daemon=True).start()
        self.send_messages(sock, event)

    def send_messages(self, sock: socket.socket, event: Event) -> None:
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
