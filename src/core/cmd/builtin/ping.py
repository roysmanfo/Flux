from ...helpers.commands import *
from ...helpers.arguments import Parser
import ping3
import socket
import time
import platform


class Stats:
    def __init__(self) -> None:
        self.counter = 0
        self.min = float('inf')
        self.max = float('-inf')
        self.p_lost = 0
        self.p_received = 0

        self.start_time = time.time()

    @property
    def avg(self):
        return round((self.max + self.min) / 2, 3)

    @property
    def loss(self):
        return round(self.p_lost / self.counter * 100, 2)
    
    @property
    def time(self):
        return int((time.time() - self.start_time) * 1000)

class Command(CommandInterface):

    def init(self):
        self.parser = Parser(prog="ping", description="send ICMP ECHO_REQUEST to network hosts")
        self.parser.add_argument("destination", help="dns name or ip address")
        self.parser.add_argument("-c", dest="count", type=int, default=4, help="stop after <count> replies, default 4")
        self.parser.add_argument("-i", dest="interval", default=1, type=float, help="seconds between sending each packet")
        self.parser.add_argument("-I", dest="interface", help="either interface name or address (Linux only)")
        self.parser.add_argument("-t", dest="ttl", default=116, type=int, help="define time to live")
        self.parser.add_argument("-s", dest="size", default=64, type=int, help="use <size> as number of data bytes to be sent")
        self.parser.add_argument("-q", dest="quiet", action="store_true", help="quiet output")
        self.parser.add_argument("-W", dest="timeout", default=3, type=int, help="time to wait for response")
        self.stats = None

    def setup(self):
        super().setup()
        if not self.status == STATUS_ERR:

            # check if the values provided make sense

            if platform.system().lower() != 'linux' and self.args.interface:
                self.args.interface = None
                self.warning("the -I option is available only in linux, switching to default interface")
            
            if self.args.count and not (1 <= self.args.count <= 9223372036854775807):
                self.error(self.errors.invalid_argument(self.args.count), "1 <= value <= 9223372036854775807")
                self.parser.exit_execution = True

            elif self.args.ttl < 1:
                self.error()
                self.parser.exit_execution = True

            elif not (0 <= self.args.ttl <= 255):
                self.error(self.errors.invalid_argument(self.args.ttl,"0 <= value <= 255"))
                self.parser.exit_execution = True
                
          
            elif not (0 <= self.args.size <= 2147483647):
                self.error(self.errors.invalid_argument(self.args.size, "0 <= value <= 2147483647"))
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
            fqdn = socket.getfqdn(self.args.destination)
        except socket.error:
            self.error("unable to determine full domain name")
            return
        
        icmp_seq = 0
        t = time.time()
        self.stats = Stats()


        try:
            while self.args.count != 0:

                if time.time() - t >= self.args.interval:
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


                    # modify stats
                    self.stats.counter += 1
                    if delay:
                        self.stats.p_received += 1
                        self.stats.max = round(max(self.stats.max, delay), 3)
                        self.stats.min = round(min(self.stats.min, delay), 3)
                    else:
                        self.stats.p_lost += 1


                    if not self.args.quiet:
                        self.print(f"{self.args.size} bytes from {fqdn} ({dest_addr}): icmp_seq={icmp_seq} ttl={self.args.ttl} time={round(delay, 1)} ms")

                    if self.args.count:
                        self.args.count -= 1

                    icmp_seq += 1
                    t = time.time()

        except KeyboardInterrupt:
            pass
    
    def close(self):
        if not self.status == STATUS_ERR:
            self.print(f"\n--- {self.args.destination} ping statistics ---")
            self.print(f"{self.stats.counter} packets transmited, {self.stats.p_received} received, {self.stats.loss}% packet loss, time {self.stats.time}ms")
            
            if self.stats.min == float("inf"):
                self.stats.min = .0
            if self.stats.max == float("-inf"):
                self.stats.max = .0

            self.print(f"rtt min/avg/max = {round(self.stats.min, 3)}/{round(self.stats.avg or 0, 3)}/{round(self.stats.max, 3)} ms")

        super().close()

 