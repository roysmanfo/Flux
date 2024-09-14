import os
from pathlib import Path
import sys
import json


from flux.core.system import loader
from flux.utils import crash_handler

class Servicemanager:
    def __init__(self, service_db_path: Path) -> None:
        # maps the service name to the corresponding object
        self.service_table: dict[str, object] = {}
        self.service_db_path = service_db_path
        self.service_db: dict[str, dict[str, str | bool]] = {}
        self.system: object = None

        if not os.path.exists(service_db_path):
            with open(service_db_path, "wt") as services_db:
                self.service_db = self._get_default_services()
                json.dump(self.service_db, services_db, sort_keys=True, indent=4)
        elif not os.path.isfile(service_db_path):
            # **please** do not create conflicts with paths
            # otherwise each time you will startwith the default
            # services and default configurations
            # which means that every time you'll have to start
            # external services or the ones that do not start by default :(
            self.service_db = self._get_default_services()
        else:
            try:
                with open(service_db_path, "rt") as services_db:
                    self.service_db = json.load(services_db)   
            except json.JSONDecodeError as e:
                print(f"an error accoured when reading '{service_db_path}' ({type(e)})", file=sys.stderr)
                _, log_path = crash_handler.write_error_log()
                print(f"The full traceback of this error can be found here: \n{log_path}\n", file=sys.stderr)

                if input("reset the file to default (N/y)").lower() != 'y':
                    print("Aborting...", file=sys.stderr)
                    sys.exit(1)
                
                try:
                    os.remove(service_db_path)
                except Exception as e:
                    # this is mainly for PermissionError,
                    # but other exceptions caused by race conditions can't be predicted
                    print(f"unable to remove '{service_db_path}' ({type(e)})", file=sys.stderr)
                    _, log_path = crash_handler.write_error_log()
                    print(f"The full traceback of this error can be found here: \n{log_path}\n", file=sys.stderr)
                    print("Aborting...", file=sys.stderr)
                    sys.exit(1)

                with open(service_db_path, "wt") as services_db:
                    self.service_db = self._get_default_services()
                    json.dump(self.service_db, services_db, sort_keys=True, indent=4)

    def _get_default_services(self) -> dict[str, dict[str, str | bool]]:
        return {"services": {}}


    def register_service(self, service_name: str) -> bool:
        """
        Register a new service

        :param service_name: the name of the service to register
        :returns: True if the service has been found and added
        """
        from ..helpers.services import ServiceInterface
        exec_service_class = loader.load_service(service_name)
        if not exec_service_class or not ServiceInterface._is_subclass(exec_service_class):
            return False
        service = exec_service_class(self.system)

        if isinstance(service, ServiceInterface):
            self.service_table.update({service.name: service})
        



    def exists(self, service_name: str) -> bool:
        """
        returns True if the specified service has been already registered

        :param service_name: the name of the service to loook for
        """
        return self.service_table.get(service_name, None) is not None


    def enable(self, name: str) -> bool:
        service = self.service_table.get(name, None)

        if service:
            service._enabled = True



    
        