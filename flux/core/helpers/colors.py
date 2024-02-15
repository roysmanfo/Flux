

class Foreground:
    def __init__(self) -> None:
        self.RESET           = "\033[0m"   
        self.BLACK           = "\033[0;30m"
        self.RED             = "\033[0;31m"
        self.GREEN           = "\033[0;32m"
        self.BLUE            = "\033[0;34m"
        self.CYAN            = "\033[0;36m"
        self.YELLOW          = "\033[1;33m"
        self.PURPLE          = "\033[0;35m"

        self.LIGHTBLACK_EX   = "\033[0;90m"
        self.LIGHTRED_EX     = "\033[0;91m"
        self.LIGHTGREEN_EX   = "\033[0;92m"
        self.LIGHTYELLOW_EX  = "\033[0;93m"
        self.LIGHTBLUE_EX    = "\033[0;94m"
        self.LIGHTMAGENTA_EX = "\033[0;95m"
        self.LIGHTCYAN_EX    = "\033[0;96m"
        self.LIGHTWHITE_EX   = "\033[0;97m"


class Background:
    def __init__(self) -> None:
        self.RESET           = "\033[0;49m"
        self.BLACK           = "\033[0;40m"
        self.RED             = "\033[0;41m"
        self.GREEN           = "\033[0;42m"
        self.YELLOW          = "\033[0;43m"
        self.BLUE            = "\033[0;44m"
        self.MAGENTA         = "\033[0;45m"
        self.CYAN            = "\033[0;46m"
        self.WHITE           = "\033[0;47m"

        self.LIGHTBLACK_EX   = "\033[0;100m"
        self.LIGHTRED_EX     = "\033[0;101m"
        self.LIGHTGREEN_EX   = "\033[0;102m"
        self.LIGHTYELLOW_EX  = "\033[0;103m"
        self.LIGHTBLUE_EX    = "\033[0;104m"
        self.LIGHTMAGENTA_EX = "\033[0;105m"
        self.LIGHTCYAN_EX    = "\033[0;106m"
        self.LIGHTWHITE_EX   = "\033[0;107m"


class Styles:
    def __init__(self) -> None:
        self.RESET_ALL = "\033[0m"
        self.BRIGHT    = "\033[1m"
        self.DIM       = "\033[2m"
        self.NORMAL    = "\033[22m"



