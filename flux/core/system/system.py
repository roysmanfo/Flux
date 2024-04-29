# from flux.settings.info import SysInfo, VERSION
from typing import Any




class PrivilegeError(PermissionError):
    ...



class PrivilegedSystem:
    """
    This version of System is only provided to commands that get run with
    elevated privileges
    """
    def __init__(self) -> None:
        self.i_handler = None
        self.allow_privileged = False


    def privileged(self, func: Any):
        """
        This decorator does not allow to run a function if the command does not have enough privileges
        """
        if not self.allow_privileged:
            raise PrivilegeError("unable to run. (low privileges)")

        def inner(*args, **kwargs):
            out = func(*args, **kwargs)
            return out
        return inner

    @privileged
    def test():
        print("hello")

# class System(PrivilegedSystem):
#     """
#     System allows to interact with multiple parts of Flux,
#     get information about versions, read, write settings, ...

#     If the command gets run with elevated privileges, PrivilegedSystem is supplied instead
#     """
#     def __init__(self, sysinfo: SysInfo) -> None:
#         self.exit = False
#         self.sysinfo = sysinfo
#         self.version = VERSION

#     def get_info(self) -> SysInfo:
#         return self.sysinfo.copy()

    
ps = PrivilegedSystem()
ps.test()


