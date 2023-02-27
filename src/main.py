# Dependencies
from threading import Thread
from utils import transform
from settings.info import User, Info, SETTINGS_FILE, SETTINGS_FOLDER
from core import setup, manager
from core.cmd import cr
import os
from colorama import init, Fore
import subprocess
import platform
import sys
init(autoreset=True)
# Cristal modules


# Setup process
INFO: Info = setup.setup(User, Info, SETTINGS_FILE, SETTINGS_FOLDER)


def listen() -> list[str]:
    """
    This function is used to get the command typed by the user preceded by
    a string of text containing the username, the name of the program,
    the version and the location where Cristal is oparating on the disk.
    """
    print(
        f"{Fore.GREEN}{INFO.user.username}{Fore.CYAN} Cristal [{INFO.version}] {Fore.YELLOW}" + str(INFO.user.paths.terminal).lower() + f"{Fore.WHITE}{Fore.MAGENTA} $ ", end="")
    command = input()
    print(f"{Fore.WHITE}", end="")

    return transform.string_to_list(command)


def run():
    while True:
        os.chdir(INFO.user.paths.terminal)
        try:
            cmd = listen()

        except KeyboardInterrupt:
            print()
            continue

        # Check if we just want to leave, there's no need to check in
        # all of SYSTEM_CMDS if we just want to leave and do it quickly
        if cmd[0] == "exit":
            os._exit(0)

        # Check if it's a command the default terminal can handle
        elif cmd[0] in INFO.system_cmds or cmd[0] == "clear":
            if cmd[0] == "cd" and len(cmd) > 1:
                try:
                    new_dir = "" + cmd[1].strip("\"").strip("'")
                    os.chdir(f"{new_dir}")
                except FileNotFoundError:
                    # Disply an error message if path specified is iniexistent
                    print("Cannot find specified path because it does not exist")
                    pass
                INFO.user.paths.terminal = os.getcwd()
                INFO.user.paths.terminal.replace("\\", "/")
            else:
                # os.system(f"cd {USER.paths.terminal} && "+" ".join(cmd))
                out = default_terminal_output(" ".join(cmd))
                if out != 1 and out != "\r":
                    print(out)

        # Otherwise it might be a Cristal command
        elif cmd[0] == "cr":
            if len(cmd) > 1:
                if cmd[1].startswith("$"):
                    cr.get_variables(INFO, cmd[1])
                else:
                    cmd.pop(0)
                    manager.manage(cmd, INFO)
            else:
                cr.description(INFO.user)

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
    - If the command doesn't have a particular output, returns "\\r"
    """

    if command.rstrip('\n') in ['cls', 'clear']:
        os.system('cls') if platform.system(
        ) == 'Windows' else os.system('clear')
        return "\r"

    pipe = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    while True:
        # Errors have higher priority
        # This is to prevent the program from searching for an output
        # that doesn't exist

        if pipe.stderr:
            return 1
        else:
            return pipe.stdout


if __name__ == "__main__":

    tasks_list: list[Thread] = [i for i in INFO.bg_tasks]
    tasks_list.append(Thread(target=run, args=(), name="Main Thread"))

    try:
        for task in tasks_list:
            task.start()

        for task in tasks_list:
            task.join()

    except KeyboardInterrupt:
        # Catch all the exceptions related to the whole program.
        # Exeptions in single commands will get handled by the command itself.

        print(f"{Fore.RED}Cristal failed to execute{Fore.RESET}")
        sys.exit(1)

    sys.exit(0)
