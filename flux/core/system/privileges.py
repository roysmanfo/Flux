from enum import IntEnum
from typing import Any, Callable


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
        if self.PRIVILEGES < Privileges.HIGH:
            raise PrivilegeError("Invalid permissions to execute method")
        return func(self, *args, **kwargs)
    return wrapper

def system_privileges(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Decorator for methods that can only be executed with system privileges
    """
    def wrapper(self, *args, **kwargs):
        if self.PRIVILEGES < Privileges.SYSTEM:
            raise PrivilegeError("This method can only be executed by the system")
        return func(self, *args, **kwargs)
    return wrapper

