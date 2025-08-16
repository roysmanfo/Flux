# External Dependencies
import sys
import os
import signal
from typing import List
from colorama import init, Fore

sys.path.append(os.path.dirname(os.getcwd()))
init(autoreset=True)

# Flux modules
from flux.core import setup, manager
from flux import utils

def listen() -> List[str]:
    """
    This function is used to get the command typed by the user preceded by
    a string of text containing the username, the name of the program,
    the version and the location where Flux is oparating on the disk.
    """
    path = SYSTEM.variables.get("$PWD").value.lower()
    home = SYSTEM.variables.get("$HOME").value.lower()
    cwd = path.replace(home, "~")
   
    try:
        print(
            f"{Fore.GREEN}{SYSTEM.settings.user.username}{Fore.CYAN} Flux [{SYSTEM.version}] {Fore.YELLOW}" + cwd + f"{Fore.MAGENTA} $ ", end="")
        command = input()
        print(f"{Fore.WHITE}", end="")

        return utils.parsing.string_to_list(command)

    except (KeyboardInterrupt, EOFError):
        signal.raise_signal(signal.SIGINT)
        print(f"{Fore.RED}^C{Fore.RESET}", file=sys.stderr)
        return []


def run():
    while not SYSTEM.exit:
        os.chdir(SYSTEM.variables.get("$PWD").value)
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
            print()
        except ValueError as e:
            print(f"-flux: {e}\n", file=sys.stderr)



def main():
    global setup
    global SYSTEM

    try:

        # Setup process
        SYSTEM = setup.setup()
        del setup # forcibly remove setup module as no longer needed

        # check for line arguments
        if len(sys.argv) > 1:
            cmd = sys.argv[1:]
            manager.manage(cmd, SYSTEM)
            return 0

        SYSTEM.processes._add_main_process(SYSTEM, ['flux'], run)
        return 0

    except Exception as e:
        # Catch all the exceptions related to the whole program.
        # Exeptions in single commands will get handled by the command itself.

        # Something REALLY weird is going on if execution reaches here

        sys.stderr.write("Failed do start\n")
        sys.stderr.write("We belive the problem might be on your system\n")
        sys.stderr.write(f"\nError message \n{'-' * 13}\n{type(e).__name__}: {e.__str__()}\n\n")

        log_path = utils.crash_handler.write_error_log()[1]
        sys.stderr.write("The full traceback of this error can be found here: \n" + log_path + "\n")

        return 1

if __name__ == "__main__":
    SYSTEM: setup.System
    sys.exit(main())
