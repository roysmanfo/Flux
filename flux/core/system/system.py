from flux.settings.info import Info, VERSION


class System:
    def __init__(self, sysinfo: Info) -> None:
        self.exit = False
        self.sysinfo = sysinfo
        self.version = VERSION

    def get_info(self) -> Info:
        return self.sysinfo.copy()

