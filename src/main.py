# Dependencies
import asyncio
from utils import transform
from settings.info import User, Info, SETTINGS_FILE, SETTINGS_FOLDER, VERSION
from core import setup, manager
from core.cmd import cr
import os
from colorama import init, Fore
import subprocess
init(autoreset=True)
# Cristal modules


# Setup process
USER, INFO = setup.setup(User, Info, SETTINGS_FILE, SETTINGS_FOLDER)

# Define the type in an absolue way
USER: User
INFO: Info

with open(INFO.lang_file, 'r') as file:
    LANG: list = file.readlines()


def listen() -> list[str]:
    """
    This function is used to get the command typed by the user preceded by
    a string of text containing the username, the name of the program,
    the version and the location where Cristal is oparating on the disk.
    """
    print(
        f"{Fore.GREEN}{USER.username}{Fore.CYAN} Cristal [{VERSION}] {Fore.YELLOW}" + str(USER.paths.terminal).lower() + f"{Fore.WHITE}{Fore.MAGENTA} $ ", end="")
    command = input()
    print(f"{Fore.WHITE}", end="")

    return transform.string_to_list(command)


async def run():
    while True:
        os.chdir(USER.paths.terminal)
        cmd = listen()

        # Check if we just want to leave, there's no need to check in
        # all of SYSTEM_CMDS if we just want to leave and do it quickly
        if cmd[0] == "exit":
            os._exit(0)

        # Check if it's a command the default terminal can handle
        elif cmd[0] in INFO.system_cmds:
            if cmd[0] == "cd" and len(cmd) > 1:
                try:
                    os.chdir(cmd[1])
                except FileNotFoundError:
                    # Disply an error message if path specified is iniexistent
                    print(LANG[1])
                    pass
                USER.paths.terminal = os.getcwd()
                USER.paths.terminal.replace("\\", "/")
            else:
                # os.system(f"cd {USER.paths.terminal} && "+" ".join(cmd))
                out = default_terminal_output(" ".join(cmd))
                if out != 1:
                    print(out)

        # Otherwise it might be a Cristal command
        elif cmd[0] == "cr":
            if len(cmd) > 1:
                cmd.pop(0)
                await manager.manage(cmd, INFO)
            else:
                cr.description(USER, INFO.lang_file)

        # Command not found, a message will be displayed based on USER.language
        else:
            pass

def default_terminal_output(command: str) -> str | int:
    """
    Tries to execute the given command using the default OS terminal.

    Parameters
    ----------
    @param command      A string containing the text command to execute


    Returns
    -------
    
    - If the command executes successfully, it returns the terminal output 
    - If the command fails it returns a 1 indicating that an error accoured
    """
    pipe = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    while True:
        # Errors have higher priority
        # This is to prevent the program from searching for an output
        # that doesn't exist

        if pipe.stderr:   
            return 1
        else:
            return pipe.stdout


if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    tasks = [i for i in INFO.bg_tasks[0]]
    tasks.append(loop.create_task(run(), name="Main Thread"))

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
