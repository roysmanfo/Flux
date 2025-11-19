from typing import Union
import os
from pathlib import Path
import sys
import json
from threading import Thread


from flux.core.system import loader
from flux.utils import crash_handler

class Servicemanager:
    def __init__(self, service_db_path: Path) -> None:
        from ..system.system import System
        from ..interfaces.services import ServiceInterface

        # maps the service name to the corresponding object
        self.service_table: dict[str, ServiceInterface] = {}        # name -> Service           (currently loaded in memory)
        self.service_db: dict[str, dict[str, str | bool]] = {}      # name -> service_data      (registered in services.json)
        self.service_db_path = service_db_path
        self.system: System = None

    def _load_service_db(self):
        if not os.path.exists(self.service_db_path):
            self.reset_service_db()
        elif not os.path.isfile(self.service_db_path):
            # **please** do not create conflicts with paths
            # otherwise each time you will startwith the default
            # services and default configurations
            # which means that every time you'll have to start
            # external services or the ones that do not start by default :(
            self.service_db = self._get_default_services()
        else:
            try:
                with open(self.service_db_path, "rt") as services_db:
                    self.service_db = json.load(services_db)   
            except json.JSONDecodeError as e:
                print(f"an error accoured when reading '{self.service_db_path}' ({type(e)})", file=sys.stderr)
                _, log_path = crash_handler.write_error_log()
                print(f"Thhe full traceback of this error can be found ere: \n{log_path}\n", file=sys.stderr)

                if input("reset the file to default (N/y): ").lower() != 'y':
                    print("Aborting...", file=sys.stderr)
                    sys.exit(1)
                
                try:
                    os.remove(self.service_db_path)
                    self.reset_service_db()
                except Exception as e:
                    # this is mainly for PermissionError,
                    # but other exceptions caused by race conditions can't be predicted
                    print(f"unable to remove '{self.service_db_path}' ({type(e)})", file=sys.stderr)
                    _, log_path = crash_handler.write_error_log()
                    print(f"The full traceback of this error can be found here: \n{log_path}\n", file=sys.stderr)
                    print("Aborting...", file=sys.stderr)
                    sys.exit(1)

    def _start_enabled_services(self):
        # get all enabled services in one go
        enabled_services = [
            service_name 
            for service_name in self.service_db 
            if self.service_db.get(service_name).get("enabled", False)
        ]
        
        for service_name in enabled_services:
            if self.register_service(service_name):
                self.service_table[service_name]._enabled = True


    def reset_service_db(self) -> None:
        """
        reset the service database to the default values
        """
        self.service_db = self._get_default_services()
        self.update_service_db()
    
    def restart(self) -> None:
        """
        reads the database, starts enabled services
        and saves their metadata in a table (`self.service_table`) 
        """
        self._load_service_db()
        self._start_enabled_services()

    def _get_default_services(self) -> dict[str, Union[str, bool]]:
        return {"sys_usage": {"enabled": True}, "net_monitor": {"enabled": True}}

    def update_service_db(self) -> None:
        """
        Write the current `service_db` into `services.json`
        """
        with open(self.service_db_path, "wt") as sdb:
            try:
                json.dump(self.service_db, sdb, sort_keys=True, indent=2)
            except json.JSONDecodeError:
                # before giving up try serializing
                # the dictionary before writing it
                sdb.write(json.dumps(self.service_db, sort_keys=True, indent=2))

    def register_service(self, service_name: str) -> bool:
        """
        Register a new service

        :param service_name: the name of the service to register
        :returns: True if the service has been found and added
        """
        from ..interfaces.services import ServiceInterface

        exec_service_class = loader.load_service(service_name)
        if not exec_service_class or not ServiceInterface._is_subclass(exec_service_class):
            return False
        service: ServiceInterface = exec_service_class(self.system, service_name)

        # make sure the service is *actually a Service* 
        if not isinstance(service, ServiceInterface):
            return False
        
        self.service_table.update({service_name: service})

        # start service
        self.start_service(service_name)

        return True

    def start_service(self, service_name: str) -> bool:
        """
        Start running a service

        :param service_name: the name of the service to start
        :param new_thread: if True, a new thread will be created for this service
        :returns: True if the service has been started 
        """
        if (service := self.service_table.get(service_name)) is None:
            # the service has not been registered
            return False
        
        if not service.running:
            Thread(target=service.start, name=service_name, daemon=True).start()

        return True

    def stop_service(self, service_name: str) -> bool:
        """
        Stop a service

        :param service_name: the name of the service to stop
        :returns: True if the service has been found and stopped 
        """
        if (service := self.service_table.get(service_name)) is None:
            # the service has not been registered
            return False
        
        if service.running:
            service.stop()
        return True

    def exists(self, service_name: str) -> bool:
        """
        returns True if the specified service has been already registered

        :param service_name: the name of the service to loook for
        """
        return self.service_table.get(service_name, None) is not None


    def enable(self, name: str) -> bool:
        """
        Modify the service's settings to set `enabled` to True

        :param name:
            the name of the service to enable
        :returns status:
            True if the service was successfully modified
        """
        service = self.get(name)
        service_info = self.get_info(name)

        if service:
            service._enabled = True
        
        if service_info:
            service_info.update({"enabled": True})
            self.service_db[name] = service_info
            self.update_service_db()
            return True
        return False

    def disable(self, name: str) -> bool:
        """
        Modify the service's settings to set `enabled` to False

        :param name:
            the name of the service to disable
        :returns status:
            True if the service was successfully modified
        """
        service = self.get(name)
        service_info = self.get_info(name)

        if service:
            service._enabled = False
        
        if service_info:
            service_info.update({"enabled": False})
            self.service_db[name] = service_info
            self.update_service_db()
            return True
        return False


    def get(self, service_name: str):
        return self.service_table.get(service_name)

    def get_info(self, service_name: str):
        return self.service_db.get(service_name)


    
        