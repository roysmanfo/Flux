from src.settings.info import Info
import sys
from typing import TextIO
from src.core.system.processes import *
from colorama import init as col_init, Fore

col_init(autoreset=True)

class CommandInterface:
    """
    Interface class for commands

    Every command that uses is equiped with the standard methods to work on the app.  \n
    Every single command should use this class to keep a consistent standard.
    
    ### GENERAL ATTRIBUTES
    Attributes shared by commands

    - `IS_PROCESS (const, bool)`     Whether or not the command is being runned as a background thread 
    - `info (variable, Info)`       A reference to the instance of the Info class, containing process information 
    - `stdout (variable, TextIO)`   The stdout of the command
    - `stderr (variable, TextIO)`   The stderr of the command
    - `stdin (variable, TextIO)`    The stdin of the command

    ### AUTOMATIC CALLS
    Methods that get called regardless by the terminal

    - `init()`      This method is called right before run().
    - `run()`       This is the entry method for the command.
    - `close()`     This is the method that gets called right after run() the command. 
    - `exit()`      This is the last method that gets called.

    ### HELPER FUNCTIONS
    Other usefull methods, NOT called by the terminal.
    If you want to use these methods you need to call them yourself.

    - `error()`     This function should be called once an error accoures.
    - `warning()`   This function should be called to issue warnings.

    """


    def __init__(self,
                 info: Info,
                 is_process: bool,
                 stdout: TextIO = sys.stdout, 
                 stderr: TextIO = sys.stdout, 
                 stdin: TextIO = sys.stdout
                ) -> None:
        
        self.IS_PROCESS: bool = is_process
        self.info: Info = info
        self.status: int | None = None
        self.stdout = stdout
        self.stderr = stderr
        self.stdin = stdin

    """
    AUTOMATIC CALLS
    """

    def init(self, *args, **kwargs):
        """
        This is function is called right before run().\n
        This function should be used to do setup operations
        """
        ...
    
    def run(self, command: list[str], *args, **kwargs):
        """
        This is the entry function for the command.\n
        This function should be used to manage arguments and adapt command execution.
        """
        ...

    def close(self):
        """
        This is the function that gets called after we run the command.\n
        This function should be used to handle cases like the command being executed as a background task,
        or to do some cleaning after the command executed.
        """
        ...

    def exit(self):
        """
        This is the last function that gets called.\n
        This function should be used to definetly close execution.
        """
        return self.status if self.status else STATUS_OK

    """
    HELPER FUNCTIONS
    """

    def error(self, status: int | None = None, msg: str | None = None, use_color: bool = False):
        """
        This function should be called once an error accoures.\n
        This function should be called to handle errors.

        By default sets the status to STATUS_ERR.
        """
        if use_color:
            self.stderr.write(f"{Fore.RED}{self.parser.prog}: {msg}{Fore.RESET}\n\n")
        else:
            self.stderr.write(f"{self.parser.prog}: {msg}\n\n")
        self.status = status or STATUS_ERR

    def warning(self, status: int | None = None, msg: str | None = None, use_color: bool = False, to_stdout: bool = True):
        """
        This function should be called to issue warnings.\n
        This function should be called to handle warnings (by default writes to stdout).

        By default sets the status to STATUS_WARN.
        """
        
        if to_stdout:
            if use_color:
                self.stdout.write(f"{Fore.YELLOW}{self.parser.prog}: {msg}{Fore.RESET}\n")
            else:
                self.stdout.write(f"{msg}\n")
        else:
            if use_color:
                self.stderr.write(f"{Fore.YELLOW}{self.parser.prog}: {msg}{Fore.RESET}\n")
            else:
                self.stderr.write(f"{msg}\n")



        self.status = status or STATUS_WARN
