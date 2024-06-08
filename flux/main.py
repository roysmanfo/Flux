# External Dependencies
import sys
import os
import signal
from typing import List
from colorama import init, Fore

sys.path.append(os.path.dirname(os.getcwd()))
init(autoreset=True)

# Flux modules
from core import setup, manager
import utils

def listen() -> List[str]:
    """
    This function is used to get the command typed by the user preceded by
    a string of text containing the username, the name of the program,
    the version and the location where Flux is oparating on the disk.
    """
    try:
        print(
            f"{Fore.GREEN}{SYSTEM.settings.user.username}{Fore.CYAN} Flux [{SYSTEM.version}] {Fore.YELLOW}" + SYSTEM.variables.get("$PWD").value.lower() + f"{Fore.MAGENTA} $ ", end="")
        command = input()
        print(f"{Fore.WHITE}", end="")

        return utils.transform.string_to_list(command)

    except (KeyboardInterrupt, EOFError):
        signal.raise_signal(signal.SIGINT)
        print(f"{Fore.RED}^C{Fore.RESET}", file=sys.stderr)
        return []


def run():
    while not SYSTEM.exit:
        os.chdir(SYSTEM.settings.user.paths.terminal)
        try:
            cmd = listen()

            if cmd:
                if cmd[0] == "exit":
                    SYSTEM.exit = True

                # Pass the command to the manager
                else:
                    if cmd[0] != "":
                        manager.manage(cmd, SYSTEM)
        except KeyboardInterrupt:
            signal.raise_signal(signal.SIGINT)

if __name__ == "__main__":
    
    try:

        # Setup process
        SYSTEM = setup.setup()
        del setup

        # check for line arguments
        if len(sys.argv) > 1:
            cmd = sys.argv[1:]
            manager.manage(cmd, SYSTEM)
            sys.exit(0)

        SYSTEM.processes._add_main_process(SYSTEM, ['flux'], run)
        sys.exit(0)

    except Exception as e:
        # Catch all the exceptions related to the whole program.
        # Exeptions in single commands will get handled by the command itself.

        # Something REALLY weird is going on if execution reaches here

        sys.stderr.write("Failed do start\n")
        sys.stderr.write("We belive the problem might be on your system\n")
        sys.stderr.write(f"\nError message \n{'-' * 13}\n{type(e).__name__}: {e.__str__()}\n\n")

        log_path = utils.crash_handler.write_error_log()[1]
        sys.stderr.write("The full traceback of this error can be found here: \n" + log_path + "\n")

        sys.exit(1)
