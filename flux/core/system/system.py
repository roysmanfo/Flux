from flux.settings.settings import Settings, VERSION
from .privileges import Privileges


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
        self.privileges = Privileges
        

    def get_info(self) -> Settings:
        return self.sysinfo.copy()
    



