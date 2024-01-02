from ...helpers.commands import *
from ...helpers.arguments import Parser
import ping3
import socket
import time
import platform


class Command(CommandInterface):

    def init(self):
        self.parser = Parser(prog="ping", description="send ICMP ECHO_REQUEST to network hosts")
        self.parser.add_argument("destination", help="dns name or ip address")
        self.parser.add_argument("-c", dest="count", type=int, help="stop after <count> replies")
        self.parser.add_argument("-i", dest="interval", default=1, type=float, help="seconds between sending each packet")
        self.parser.add_argument("-I", dest="interface", help="either interface name or address (Linux only)")
        self.parser.add_argument("-t", dest="ttl", default=116, type=int, help="define time to live")
        self.parser.add_argument("-s", dest="size", default=64, type=int, help="use <size> as number of data bytes to be sent")
        self.parser.add_argument("-q", dest="quiet", action="store_true", help="quiet output")
        self.parser.add_argument("-W", dest="timeout", default=3, type=int, help="time to wait for response")

    def setup(self):
        super().setup()
        if not self.parser.exit_execution:

            # check if the values provided make sense

            if platform.system().lower() != 'linux' and self.args.interface:
                self.args.interface = None
                self.warning("the -I option is available only in linux, switching to default interface")
            
            if self.args.count and not (1 <= self.args.count <= 9223372036854775807):
                self.error(self.logger.invalid_argument(self.args.count), "1 <= value <= 9223372036854775807")
                self.parser.exit_execution = True

            elif self.args.ttl < 1:
                self.error()
                self.parser.exit_execution = True

            elif not (0 <= self.args.ttl <= 255):
                self.error(self.logger.invalid_argument(self.args.ttl,"0 <= value <= 255"))
                self.parser.exit_execution = True
                
          
            elif not (0 <= self.args.size <= 2147483647):
                self.error(self.logger.invalid_argument(self.args.size, "0 <= value <= 2147483647"))
                self.parser.exit_execution = True
                
            
            elif self.args.timeout < 0:
                self.error(f"bad linger time: {self.args.timeout}")
                self.parser.exit_execution = True
                


    def run(self):
        try:
            dest_addr = socket.gethostbyname(self.args.destination)

        except socket.error:
            self.error("unable to resolve destination ip address")
            return
        
        self.print(f"PING {self.args.destination} ({dest_addr}) 56(84) bytes of data.")
        
        try:
            self.args.destination = socket.getfqdn(self.args.destination)
        except socket.error:
            self.error("unable to determine full domain name")
            return
        
        icmp_seq = 0
        t = time.time()

        try:
            while self.args.count != 0:

                if time.time() - t >= self.args.timeout:
                    delay = ping3.ping(
                        dest_addr=dest_addr,
                        timeout=self.args.timeout,
                        unit="ms",
                        src_addr=None,
                        ttl=self.args.ttl,
                        seq=icmp_seq,
                        size=self.args.size,
                        interface=self.args.interface
                    )

                    if not self.args.quiet:
                        self.print(f"{self.args.size} bytes from {self.args.destination} ({dest_addr}): icmp_seq={icmp_seq} ttl={self.args.ttl} time={round(delay, 1)} ms")

                    if self.args.count:
                        self.args.count -= 1

                    icmp_seq += 1
                    t = time.time()

        except KeyboardInterrupt:
            pass



 