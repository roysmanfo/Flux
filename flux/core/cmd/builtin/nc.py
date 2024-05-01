from ...helpers.commands import *
from ...helpers.arguments import Parser

import socket

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
            sock.send(b"this is some data")






