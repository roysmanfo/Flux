from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)



class Command(CommandInterface):
    def init(self) -> None:
        self.parser = Parser(
            prog="systemctl",
            description="Query or send control commands to the system manager.",
            usage="systemctl [OPTIONS...] COMMAND ...")
        
        commands = self.parser.add_subparsers(title="Unit Commands", dest="command")
        # start a service
        parser_start = commands.add_parser("start", description="Start (activate) one or more units", help="Start (activate) one or more units")
        parser_start.add_argument("units", metavar="UNITs", nargs="+", help="the services to start")
        # stop a service
        parser_stop = commands.add_parser("stop", description="Stop (deactivate) one or more units", help="Stop (deactivate) one or more units")
        parser_stop.add_argument("units", metavar="UNIT", nargs="+", help="the services to stop")


    def run(self) -> None:

        if not self.args.command:
            self.args.command = "list-units"

        match self.args.command:
            case "start": self.start_service()
            case "stop": self.stop_service()
            case _: self.error(f"Unknown command verb '{self.args.command}'", use_color=True)        
    
    # systemctl start [service_name, ...]
    def start_service(self):
        for unit in self.args.units:
            unit: str = unit.removesuffix(".service")
            
            # check if the service is already running
            if self.system.service_manager.exists(unit):
                if not self.system.service_manager.get(unit).running:
                    self.system.service_manager.start_service(unit)
                    self.print(f"{unit}.service is now running")
                else:
                    self.warning(f"{unit}.service is already running", use_color=True)
                continue

            status = self.system.service_manager.register_service(unit)
            if not status:
                self.error(f"Failed to start {unit}.service", use_color=True)
                continue
            self.print(f"{unit}.service is now running")

    # systemctl stop [service_name, ...]
    def stop_service(self):
        for unit in self.args.units:
            unit: str = unit.removesuffix(".service")
            
            if self.system.service_manager.exists(unit):
                if self.system.service_manager.get(unit).running:
                    status = self.system.service_manager.stop_service(unit)
                    if not status:
                        self.error(f"{unit}.service not found", use_color=True)
                        continue
                    self.print(f"{unit}.service is no longer running")
                else:
                    self.warning(f"{unit}.service is already not running", use_color=True)
                continue

