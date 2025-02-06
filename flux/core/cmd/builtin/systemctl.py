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
        # disable a service
        parser_disable = commands.add_parser("disable", description="Disable one or more units", help="Disable one or more units")
        parser_disable.add_argument("units", metavar="UNIT", nargs="+", help="the services to disable")
        # start a service
        parser_start = commands.add_parser("start", description="Start (activate) one or more units", help="Start (activate) one or more units")
        parser_start.add_argument("units", metavar="UNITs", nargs="+", help="the services to start")
        # stop a service
        parser_stop = commands.add_parser("stop", description="Stop (deactivate) one or more units", help="Stop (deactivate) one or more units")
        parser_stop.add_argument("units", metavar="UNIT", nargs="+", help="the services to stop")
        # list all services
        commands.add_parser("list", description="List units currently in memory", help="List units currently in memory")
        # enable a service
        parser_enable = commands.add_parser("enable", description="Enable one or more units", help="Enable one or more units")
        parser_enable.add_argument("units", metavar="UNIT", nargs="+", help="the services to enable")
        # reset database
        commands.add_parser("reset", description="Reset the database to its default values", help="Reset the database to its default values")


    def run(self) -> None:

        if not self.args.command:
            self.args.command = "list"

        match self.args.command:
            case "disable": self.disable_service()
            case "enable": self.enable_service()
            case "list": self.list_service()
            case "start": self.start_service()
            case "reset": self.reset_db()
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
    
    # systemctl stop [service_name, ...]
    def list_service(self):
        from flux.utils import format

        if not (service_table := self.system.service_manager.service_table):
            self.warning('No services running', use_color=True)
            return

        service_data = [(s.name, s.enabled, s.running, s.metadata.get("description"))
                        for s in service_table.values()]

        table = format.create_table("name", "enabled", "running", "description", rows=service_data)
        self.print(table)
    
    # systemctl enable [service_name, ...]
    def enable_service(self):
        for unit in self.args.units:
            unit: str = unit.removesuffix(".service")
            if self.system.service_manager.get_info(unit):
                if self.system.service_manager.enable(unit):
                    self.print(f"{unit}.service has been enabled")
                else:
                    self.print(f"{unit}.service has been NOT been enabled")
            else:
                self.error(f"{unit}.service not found", use_color=True)

    # systemctl disable [service_name, ...]
    def disable_service(self):
        for unit in self.args.units:
            unit: str = unit.removesuffix(".service")
            if self.system.service_manager.get_info(unit):
                if self.system.service_manager.disable(unit):
                    self.print(f"{unit}.service has been disabled")
                else:
                    self.print(f"{unit}.service has been NOT been disabled")

            else:
                self.error(f"{unit}.service not found", use_color=True)

    # systemctl reset
    def reset_db(self):
        self.system.service_manager.reset_service_db()
        self.print("Database has been reset")
