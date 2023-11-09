
# Wheater the output is being redirected,
# If this is the case, then disable colors and reset to default
to_file = False


class Foreground:
    def __init__(self, to_file: bool) -> None:
        self.RESET           = "\033[0m"     if not to_file else ""
        self.RED             = "\033[0;31m"  if not to_file else ""
        self.GREEN           = "\033[0;32m"  if not to_file else ""
        self.BLUE            = "\033[0;34m"  if not to_file else ""
        self.CYAN            = "\033[0;36m"  if not to_file else ""
        self.YELLOW          = "\033[1;33m"  if not to_file else ""
        self.PURPLE          = "\033[0;35m"  if not to_file else ""

        self.LIGHTBLACK_EX   = "\033[0;90m"  if not to_file else ""
        self.LIGHTRED_EX     = "\033[0;91m"  if not to_file else ""
        self.LIGHTGREEN_EX   = "\033[0;92m"  if not to_file else ""
        self.LIGHTYELLOW_EX  = "\033[0;93m"  if not to_file else ""
        self.LIGHTBLUE_EX    = "\033[0;94m"  if not to_file else ""
        self.LIGHTMAGENTA_EX = "\033[0;95m"  if not to_file else ""
        self.LIGHTCYAN_EX    = "\033[0;96m"  if not to_file else ""
        self.LIGHTWHITE_EX   = "\033[0;97m"  if not to_file else ""


class Background:
    def __init__(self, to_file: bool) -> None:
        self.RESET           = "\033[0;49m"  if not to_file else ""
        self.BLACK           = "\033[0;40m"  if not to_file else ""
        self.RED             = "\033[0;41m"  if not to_file else ""
        self.GREEN           = "\033[0;42m"  if not to_file else ""
        self.YELLOW          = "\033[0;43m"  if not to_file else ""
        self.BLUE            = "\033[0;44m"  if not to_file else ""
        self.MAGENTA         = "\033[0;45m"  if not to_file else ""
        self.CYAN            = "\033[0;46m"  if not to_file else ""
        self.WHITE           = "\033[0;47m"  if not to_file else ""

        self.LIGHTBLACK_EX   = "\033[0;100m" if not to_file else ""
        self.LIGHTRED_EX     = "\033[0;101m" if not to_file else ""
        self.LIGHTGREEN_EX   = "\033[0;102m" if not to_file else ""
        self.LIGHTYELLOW_EX  = "\033[0;103m" if not to_file else ""
        self.LIGHTBLUE_EX    = "\033[0;104m" if not to_file else ""
        self.LIGHTMAGENTA_EX = "\033[0;105m" if not to_file else ""
        self.LIGHTCYAN_EX    = "\033[0;106m" if not to_file else ""
        self.LIGHTWHITE_EX   = "\033[0;107m" if not to_file else ""


class Styles:
    def __init__(self, to_file: bool) -> None:
        self.RESET_ALL = "\033[0m"           if not to_file else ""
        self.BRIGHT    = "\033[1m"           if not to_file else ""
        self.DIM       = "\033[2m"           if not to_file else ""
        self.NORMAL    = "\033[22m"          if not to_file else ""



