import os
from colorama import init, Fore
init(autoreset=True)

from core import setup
from settings.info import User, Path

setup_result = setup.setup(user=User, path=Path)

USER: User = setup_result[0]
PATH: Path = setup_result[1]
VERSION: str = setup_result[2]

def listen():
    """
    This function is used to get the command typed by the user preceded by
    a string of text containing the username, the name of the program,
    the version and the location where Cristal is oparating on the disk.
    """
    print(f"{Fore.GREEN}{USER.username}{Fore.CYAN} Cristal [{VERSION}] {Fore.YELLOW}{PATH.terminal}{Fore.WHITE} ", end="")
    command = input(f"$ ")
    return command

listen()