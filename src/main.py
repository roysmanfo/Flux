# Dependencies
import asyncio
from utils import transform, builtincmds
from settings.info import User, Path, SETTINGS_FILE, SETTINGS_FOLDER, VERSION
from core import setup, manager
from core.cmd import cr, observer
import os
import platform
from colorama import init, Fore
init(autoreset=True)
# Cristal modules


# Setup process
setup_result = setup.setup(user=User, path=Path)
USER: User = setup_result[0]
PATH: Path = setup_result[1]


if platform.system() == "Windows":
    # These commands will be executed from the default OS terminal (cmd.exe)
    SYSTEM_CMDS = builtincmds.WINDOWS
    LANG_FILE: str = os.path.join(os.path.dirname(
        __file__)+"\\lang\\", USER.language + ".txt")

elif platform.system() in ["Linux", "Mac"]:
    # These commands will be executed from the default OS terminal (linux terminal)
    SYSTEM_CMDS = builtincmds.LINUX
    LANG_FILE: str = os.path.join(os.path.realpath(
        __file__)+"/lang/", USER.language + ".txt")


def listen() -> list[str]:
    """
    This function is used to get the command typed by the user preceded by
    a string of text containing the username, the name of the program,
    the version and the location where Cristal is oparating on the disk.
    """
    print(
        f"{Fore.GREEN}{USER.username}{Fore.CYAN} Cristal [{VERSION}] {Fore.YELLOW}" + PATH.terminal.lower() + f"{Fore.WHITE}{Fore.MAGENTA} $ ", end="")
    command = input()
    print(f"{Fore.WHITE}", end="")

    return transform.string_to_list(command)


async def run():
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

                if platform.system() == "Windows":
                    PATH.terminal.replace("/", "\\")
            else:
                os.system(f"cd {PATH.terminal} && "+" ".join(cmd))

        # Otherwise it might be a Cristal command
        elif cmd[0] == "cr":
            if len(cmd) > 1:
                cmd.pop(0)
                await manager.manage(cmd, [USER, PATH, LANG_FILE, SETTINGS_FILE, SETTINGS_FOLDER])
            else:
                cr.run(USER, LANG_FILE)

        # Command not found, a message will be displayed based on USER.language
        else:
            pass


loop = asyncio.new_event_loop()

tasks = [
    loop.create_task(observer.run([USER, PATH, LANG_FILE, SETTINGS_FILE, SETTINGS_FOLDER])),
    loop.create_task(run()),
]

loop.run_until_complete(asyncio.wait(tasks))
loop.close()