# Dependencies
from utils import transform, builtincmds
from settings.info import User, Path, SETTINGS_FILE, SETTINGS_FOLDER, VERSION
from core import setup, manager
import os
import platform
from colorama import init, Fore
init(autoreset=True)

# Cristal modules

# These commands will be executed from the default OS terminal (es. cmd.exe on windows)
if platform.system() == "Windows":
    SYSTEM_CMDS = builtincmds.WINDOWS
elif platform.system() in ["Linux", "Mac"]:
    SYSTEM_CMDS = builtincmds.LINUX

# Setup process
setup_result = setup.setup(user=User, path=Path)

USER: User = setup_result[0]
PATH: Path = setup_result[1]

def listen() -> list:
    """
    This function is used to get the command typed by the user preceded by
    a string of text containing the username, the name of the program,
    the version and the location where Cristal is oparating on the disk.
    """
    print(
        f"{Fore.GREEN}{USER.username}{Fore.CYAN} Cristal [{VERSION}] {Fore.YELLOW}{PATH.terminal}{Fore.WHITE}{Fore.MAGENTA} $ ", end="")
    command = input()
    print(f"{Fore.WHITE}", end="")

    return transform.string_to_list(command)


def run():
    while True:
        os.chdir(PATH.terminal)
        cmd = listen()

        # Check if we just want to leave, there's no need to check in  
        # all of SYSTEM_CMDS if we just want to leave and do it quickly
        if cmd[0] == "exit":
            os._exit(0)

        # Check if it's a command the default terminal can handle
        elif cmd[0] in SYSTEM_CMDS:
            if cmd[0] == "cd" and len(cmd) > 1:
                os.chdir(cmd[1])
                PATH.terminal = os.getcwd()
            else:
                os.system(f"cd {PATH.terminal} && "+" ".join(cmd))

        # Otherwise it might be a Cristal command
        elif cmd[0] == "cr":
            cmd.pop(0)
            manager.manage(cmd)
        
        # Command not found, a message will be displayed based on USER.language
        else:
            pass

if __name__ == "__main__":
    run()
