import os
from flux.core.system import loader
from flux.core.system.interrupts import InterruptHandler
from flux.core.system.processes import Processes
from flux.core.system.service_manager import Servicemanager
from flux.core.system.variables import Variables
from flux.settings.settings import Settings, VERSION
from .privileges import Privileges


class System():
    """
    System allows to interact with multiple parts of Flux,
    get information about versions, read, write settings, ...

    If the command gets run with elevated privileges, PrivilegedSystem is supplied instead    
    """
    def __init__(self, settings: Settings) -> None:
        self.exit = False
        self.settings = settings
        self.version = VERSION
        self.privileges = Privileges
        self.interrupt_handler: InterruptHandler = InterruptHandler()
        self.variables: Variables = Variables()
        self.processes: Processes = Processes(self.interrupt_handler)
        self.service_manager: Servicemanager = Servicemanager(settings.syspaths.SERVICES_FILE)
        self.command_loader = loader

        self._init_reserved_variables()
        self._init_service_manager()
        
    def _init_reserved_variables(self) -> None:
        self.variables.add("$HOME", str(self.settings.user.paths.terminal).replace("\\", "/"), True)
        self.variables.add("$PATH", os.environ.get("PATH", ""), True)
        self.variables.add("$PWD", self.variables.get("$HOME").value, True)
        self.variables.add("$OLDPWD", self.variables.get("$PWD").value, True)

        for var in os.environ:
            self.variables.add("$"+var, os.environ[var], True)

    def _init_service_manager(self) -> None:
        self.service_manager.system = self
        self.service_manager.restart()

    def get_settings(self) -> Settings:
        return self.settings.copy()
    



