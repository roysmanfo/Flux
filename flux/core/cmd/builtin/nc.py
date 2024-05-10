from ...helpers.commands import *
from ...helpers.arguments import Parser

import socket
from threading import Thread, Event

ENTRY_POINT = "Netcat"

class Netcat(CommandInterface):
    def init(self):
        self.parser = Parser("nc", usage="usage: nc [options] [destination] [port]", description="arbitrary TCP and UDP connections and listens")
        self.parser.add_argument("destination", nargs="?")
        self.parser.add_argument("port", nargs="?")
        self.parser.add_argument("-4", dest="ipv4", action="store_true", default=True, help="Use IPv4")
        self.parser.add_argument("-6", dest="ipv6", action="store_true", help="Use IPv6")
        self.parser.add_argument("-l", action="store_true", help="Listen mode, for inbound connects")
        self.parser.add_argument("-n", dest="no_name_resolution", action="store_true", help="Suppress name/port resolutions")
        self.parser.add_argument("-p", dest="PORT", help="Specify local port for remote connects")
        self.parser.add_argument("-I", dest="length", default=4094, type=int, help="TCP receive buffer length")
        self.parser.add_argument("-v", dest="verbose", action="store_true", help="Verbose")

        if not self.command[1:]:
            self.command.append("-h")

    def setup(self):
        super().setup()

        if self.status == STATUS_ERR:
            return
        
        self.log_level = self.levels.DEBUG if self.args.verbose else self.levels.INFO

        if self.args.l:
            if not self.args.PORT:
                self.error("missing port number")
                return

            self.args.port = self.args.PORT
            

    def run(self):

        family = socket.AF_INET
        if self.args.ipv6:
            family = socket.AF_INET6

        with socket.socket(family, socket.SOCK_STREAM) as sock:
            self.args.port = int(self.args.port)

            if self.args.l:
                self.host_as_server(sock)
            else:
                self.host_as_client(sock)

    def host_as_server(self, sock: socket.socket) -> None:
        event = Event()
        bind_ip = "0.0.0.0" if not self.args.ipv6 else "::"
        
        sock.bind((bind_ip, self.args.port))
        sock.listen(5)

        self.debug(f"Listening on {bind_ip} {self.args.port}")
        client, addr = sock.accept()

        try:
            addr = socket.getnameinfo(addr, 0) if not self.args.no_name_resolution else addr
        except socket.gaierror:
            pass

        self.debug(f"Connection received on {addr[0]} {addr[1]}")
        Thread(target=self.recv_messages, args=(client, event), daemon=True).start()
        self.send_messages(client, event)

    def host_as_client(self, sock: socket.socket) -> None:
        event = Event()
        try:
            sock.connect((self.args.destination, self.args.port))

        except TimeoutError:
            print() # helps in understanding that the command did run
            self.status = STATUS_ERR
            return

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

        except (KeyboardInterrupt, ConnectionAbortedError, OSError):
            pass
        finally:
            event.set()


    def recv_messages(self, sock: socket.socket, event: Event) -> None:
        try:
            while not event.is_set():
                recv = sock.recv(self.args.length)
                if recv:
                    self.print(recv.decode(), end="")
                else:
                    event.set()
        except (KeyboardInterrupt, ConnectionAbortedError, OSError):
            pass
        finally:
            event.set()
