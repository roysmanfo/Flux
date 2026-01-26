try:
    from enum import StrEnum
except ImportError:
    from enum import Enum 
    class StrEnum(str, Enum):
        pass

class Foreground(StrEnum):
    RESET           = "\033[0m"   
    BLACK           = "\033[0;30m"
    RED             = "\033[0;31m"
    GREEN           = "\033[0;32m"
    BLUE            = "\033[0;34m"
    CYAN            = "\033[0;36m"
    YELLOW          = "\033[1;33m"
    PURPLE          = "\033[0;35m"

    LIGHTBLACK_EX   = "\033[0;90m"
    LIGHTRED_EX     = "\033[0;91m"
    LIGHTGREEN_EX   = "\033[0;92m"
    LIGHTYELLOW_EX  = "\033[0;93m"
    LIGHTBLUE_EX    = "\033[0;94m"
    LIGHTMAGENTA_EX = "\033[0;95m"
    LIGHTCYAN_EX    = "\033[0;96m"
    LIGHTWHITE_EX   = "\033[0;97m"


class Background(StrEnum):
    RESET           = "\033[0;49m"
    BLACK           = "\033[0;40m"
    RED             = "\033[0;41m"
    GREEN           = "\033[0;42m"
    YELLOW          = "\033[0;43m"
    BLUE            = "\033[0;44m"
    MAGENTA         = "\033[0;45m"
    CYAN            = "\033[0;46m"
    WHITE           = "\033[0;47m"
    
    LIGHTBLACK_EX   = "\033[0;100m"
    LIGHTRED_EX     = "\033[0;101m"
    LIGHTGREEN_EX   = "\033[0;102m"
    LIGHTYELLOW_EX  = "\033[0;103m"
    LIGHTBLUE_EX    = "\033[0;104m"
    LIGHTMAGENTA_EX = "\033[0;105m"
    LIGHTCYAN_EX    = "\033[0;106m"
    LIGHTWHITE_EX   = "\033[0;107m"

class Styles(StrEnum):
    RESET_ALL = "\033[0m"
    BRIGHT    = "\033[1m"
    DIM       = "\033[2m"
    NORMAL    = "\033[22m"



