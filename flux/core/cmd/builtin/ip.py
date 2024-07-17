from flux.core.helpers.commands import (
    CommandInterface,
    Parser,
    Status
)

import os
import psutil, socket


AF_LINK = socket.AF_PACKET if os.name != 'nt' else socket.AF_LINK

available_commands = {"address", "help"}

class Command(CommandInterface):
    
    def init(self):
        self.parser = Parser("ip", description="show / manipulate routing, network devices, interfaces and tunnels")
        self.parser.usage = " ip [ OPTIONS ] OBJECT { COMMAND | help }"
        self.parser.add_argument("command", help="command to execute")
        self.choosed_command = None

    def setup(self):
        super().setup()

        if not self.status == Status.STATUS_ERR:
            for command in available_commands:
                if command.startswith(self.args.command):
                    self.choosed_command = command
                    break
            else:
                self.error(f'Object "{self.args.command}" is unknown, try "ip help"')

    def run(self):
        match self.choosed_command:
            case "address":
                self.address()
            case "help":
                self.help()
                            

    def address(self):
        interfaces = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        counter = 0
        for interface, addresses in interfaces.items():

            header = f"{counter}: {interface}:"
            counter += 1


            # Retrieve the NIC stats
            if interface in stats:
                nic_stats = stats[interface]
                header += f" mtu: {nic_stats.mtu}"
                header += f" state: {'UP' if nic_stats.isup else 'DOWN'}"
            print(header)


            for address in addresses:
                broadcast = address.broadcast if address.broadcast != "None" else None
                netmask = address.netmask
                if netmask:
                    if netmask.count(":") > 0:
                        netmask = bin(int.from_bytes(bytes.fromhex(netmask.replace(":", "").replace("-", "")), "big")).count("1")
                    else:
                        netmask = sum((bin(int(i))).count("1") for i in netmask.split("."))

                
                if address.family == AF_LINK:
                    print(f"    link/ether {address.address} brd ff:ff:ff:ff:ff:ff")   
                else:

                    out = "   " + " " * (len(str(counter)) - 1)

                    match address.family:
                        case socket.AF_INET: out += f"inet"
                        case socket.AF_INET6: out += f"inet6"
                        case _:
                            if address.family.name == "AF_LINK":
                                out += f"mac"
                            else:
                                out += f"[family {address.family}]"
                                

                    addr = address.address
                    if "%" in address.address:
                        addr = address.address[:address.address.index('%')]
                    out += f" {addr}"

                    if netmask:
                        out += f"/{netmask}"
                    
                    if broadcast:
                        out += f" brd {broadcast}"

                    print(out)
            print()


    def help(self):
        self.print(self.parser.format_help())
