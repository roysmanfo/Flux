from src.settings.info import Info
import sys
from typing import TextIO
from src.core.system.processes import *
from colorama import init as col_init, Fore
from .arguments import Parser
from argparse import Namespace

col_init(autoreset=True)


class CommandInterface:
    """
    Interface class for commands

    Every command that uses is equiped with the standard methods to work on the app.  \n
    Every single command should use this class to keep a consistent standard.

    ### GENERAL ATTRIBUTES
    Attributes shared by commands

    - `IS_PROCESS (const, bool)`        Whether or not the command is being runned as a background thread 
    - `info (variable, Info)`           A reference to the instance of the Info class, containing process information 
    - `command (variable, list[str])`   The full command typed by the user (also contains the command name, es. ['ls', 'some_path'])
    - `stdout (variable, TextIO)`       The stdout of the command
    - `stderr (variable, TextIO)`       The stderr of the command
    - `stdin (variable, TextIO)`        The stdin of the command
    - `parser (variable, Parser)`       A program targeted implementation of argparse.ArgumentParser
    - `args (variable, Namespace)`      The usual output returned by ArgumentParser.parse_args
    - `logger (variable, Logger)`       Standardized handler for error/warning messages

    ### AUTOMATIC CALLS
    Methods that get called regardless by the terminal

    - `init()`      This function is called on start of execution.
    - `setup()`     This is function is called right before run().
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
                 command: list[str],
                 is_process: bool,
                 stdout: TextIO = sys.stdout,
                 stderr: TextIO = sys.stdout,
                 stdin: TextIO = sys.stdout
                 ) -> None:

        self.IS_PROCESS: bool = is_process
        self.info: Info = info
        self.command: list[str] = command
        self.status: int | None = None
        self.stdout = stdout
        self.stderr = stderr
        self.stdin = stdin
        self.parser: Parser = None
        self.args: Namespace = None
        self.logger: Logger = Logger()

    """
    AUTOMATIC CALLS
    """

    def init(self):
        """
        This function is called on start of execution.\n
        This function should be used to do setup operations (like create the Parser)
        """
        ...

    def setup(self):
        """
        This is function is called right before run().\n
        This function is used to parse arguments and exit on parsing errors
        """
        try:
            self.args = self.parser.parse_args(self.command[1:])

            if self.parser.exit_execution:
                print()
                return
        except AttributeError:
            self.args = None

    def run(self):
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
        This function should be used to define what status code to return
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
            self.stderr.write(
                f"{Fore.RED}{self.parser.prog}: {msg}{Fore.RESET}\n\n")
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
                self.stdout.write(
                    f"{Fore.YELLOW}{self.parser.prog}: {msg}{Fore.RESET}\n")
            else:
                self.stdout.write(f"{msg}\n")
        else:
            if use_color:
                self.stderr.write(
                    f"{Fore.YELLOW}{self.parser.prog}: {msg}{Fore.RESET}\n")
            else:
                self.stderr.write(f"{msg}\n")

        self.status = status or STATUS_WARN


class Logger():
    """
    Standardized handler for error/warning messages

    By default `self.path` is an empty string and 
    will be used if no path is given as function argument,

    You can change its value in the `run` function

    ```
    def run(self):    
        self.args = self.parser.parse_args(self.command[1:])
        self.logger.path = self.args.PATH
    ```

    or by recreating the object in your setup 

    ```
    def init(self):
        self.logger = Logger(PATH)
    ```

    otherwise you will have to provide the path on each call

    ```
    try:
        # Some operations
    except PermissionError:
        self.error(STATUS_ERR, self.logger.permission_error(PATH))
    ```
    """

    def __init__(self, path: str | os.PathLike | None = None) -> None:
        self.path = path or ""

    def path_not_found(self, path: str | os.PathLike | None = None):
        return f"cannot open `{path or self.path}` (No such file or directory)"

    def file_not_found(self, path: str | os.PathLike | None = None):
        return self.path_not_found(path)
            
    def permission_denied(self, path: str | os.PathLike | None = None):
        return f"cannot open `{path or self.path}` (permission denied)"

    def file_exists(self, path: str | os.PathLike | None = None):
        return f"cannot create directory `{path or self.path}`: File exists"

    def cannot_remove_dir(self, path: str | os.PathLike | None = None):
        return f"cannot remove `{path or self.path}`: Is a directory"

    def same_file(self, path1: str | os.PathLike | None = None, path2: str | os.PathLike | None = None):
        return f"`{path1 or self.path}` and `{path2 or path1 or self.path}` are the same file"
    
