# Flux modules
from core.cmd import flux
from core import setup, manager
from settings.info import User, Info, SETTINGS_FILE, SETTINGS_FOLDER
from utils import transform

# External Dependencies
import sys
import os
from threading import Thread
from colorama import init, Fore
init(autoreset=True)


# Setup process
INFO: Info = setup.setup(User, Info, SETTINGS_FILE, SETTINGS_FOLDER)
HOME_PATH = INFO.user.paths.terminal

def listen() -> list[str]:
    """
    This function is used to get the command typed by the user preceded by
    a string of text containing the username, the name of the program,
    the version and the location where Flux is oparating on the disk.
    """
    try:
        print(
            f"{Fore.GREEN}{INFO.user.username}{Fore.CYAN} Flux [{INFO.version}] {Fore.YELLOW}" + str(INFO.user.paths.terminal).lower() + f"{Fore.WHITE}{Fore.MAGENTA} $ ", end="")
        command = input()
        print(f"{Fore.WHITE}", end="")

        return transform.string_to_list(command)
    
    except KeyboardInterrupt:
        print(f"{Fore.RESET}^C")
        return transform.string_to_list("")

    except EOFError:
        print(f"{Fore.RESET}^C")
        return transform.string_to_list("")

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
            sys.exit(0)

        # Check if it's a command the default terminal can handle
        if cmd[0] == "clear":
            os.system("cls || clear")
        
        elif cmd[0] == "cd":
            if len(cmd) > 1:
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
                os.chdir(HOME_PATH)

        # Otherwise it might be a Flux command
        elif cmd[0] == "flux":
            if len(cmd) > 1:
                flux.run(INFO, cmd)
            else:
                flux.description(INFO.user)

        # Pass the command to the manager
        else:
            manager.manage(cmd, INFO)

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

        # print(f"{Fore.RED}Flux failed to execute{Fore.RESET}")
        sys.exit(1)

    sys.exit(0)
