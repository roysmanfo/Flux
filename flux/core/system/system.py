from typing import Any, Callable
from flux.settings.settings import Settings, VERSION
from enum import IntEnum

class PrivilegeError(PermissionError):
    ...


class Privileges(IntEnum):
    LOW = 10
    HIGH = 20
    SYSTEM = 30


def high_privileges(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Decorator for methods that can only be executed with high/system privileges
    """
    def wrapper(self, *args, **kwargs):
        if self.PERMISSIONS < Privileges.HIGH:
            raise PrivilegeError("Invalid permissions to execute method")
        return func(self, *args, **kwargs)
    return wrapper

def system_privileges(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Decorator for methods that can only be executed with high privileges
    """
    def wrapper(self, *args, **kwargs):
        if self.PERMISSIONS < Privileges.SYSTEM:
            raise PrivilegeError("This method can only be executed by the system")
        return func(self, *args, **kwargs)
    return wrapper


class System():
    """
    System allows to interact with multiple parts of Flux,
    get information about versions, read, write settings, ...

    If the command gets run with elevated privileges, PrivilegedSystem is supplied instead
    """
    def __init__(self, sysinfo: Settings) -> None:
        self.exit = False
        self.sysinfo = sysinfo
        self.version = VERSION
        

    def get_info(self) -> Settings:
        return self.sysinfo.copy()
    



