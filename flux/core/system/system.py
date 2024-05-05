import os
from flux.core.system.interrupts import InterruptHandler
from flux.core.system.processes import Processes
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
        
        self._init_reserved_variables()
        
    def _init_reserved_variables(self) -> None:

        self.variables.add("$ALL", "$ALL:$HOME:$PATH:$PWD", True)
        self.variables.add("$HOME", str(self.settings.user.paths.terminal), True)
        self.variables.add("$PATH", os.environ.get("PATH", ""), True)
        self.variables.add("$PWD", str(self.settings.user.paths.terminal), True)

    def get_settings(self) -> Settings:
        return self.settings.copy()
    



