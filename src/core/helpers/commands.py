import os as _os
from src.settings.info import Info
import sys
from typing import Any, TextIO
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

    - `init()`          This function is called on start of execution.
    - `setup()`         This is function is called right before run().
    - `run()`           This is the entry method for the command.
    - `close()`         This is the method that gets called right after run() the command.
    - `exit()`          This is the last method that gets called.
    - `fail_safe()`     This function gets called to capture unhandled exception.

    ### HELPER FUNCTIONS
    Other usefull methods, NOT called by the terminal.
    If you want to use these methods you need to call them yourself.

    - `error()`     This function should be called once an error accoures.
    - `warning()`   This function should be called to issue warnings.
    - `input()`     This is similar to python's `input()`, but uses `self.stdin` to not have to modify `sys.stdin` .

    """

    def __init__(self,
                 info: Info,
                 command: list[str],
                 is_process: bool,
                 stdout: TextIO = sys.stdout,
                 stderr: TextIO = sys.stdout,
                 stdin: TextIO = sys.stdin
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

    def fail_safe(self, exception: Exception):
        """
        This function gets called to capture unhandled exception.\n
        This function may be called at any time, and once called command execution will be terminated without
        `self.close()` or `self.exit()`

        By default creates a crash report as a temp file for the user to see with all the Traceback informations
        and sets `self.status` to `STATUR_ERR`
        """
        from src.utils.crash_handler import write_error_log
        prefx = self.parser.prog if self.parser else self.command[0]
        prefx += '_'
        
        if prefx == '_':
            prefx = None
        
        tmp = write_error_log(prefx)[1]

        self.stderr.write(f"An error accoured while trying to execute command  ({type(exception).__name__})\n")
        self.stderr.write(f"The full error log can be found here: \n{tmp}\n\n")
        self.status = STATUS_ERR
        

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

    def input(self, __prompt: object = "") -> str | None:
        """
        This function is used to get an input from the standard input
        and returns it as a string (if a Ctrl-c is detected, returns None).
        """
        
        try:
            if __prompt:
                self.stdout.write(__prompt)

            file_contents = self.stdin.readline()
            return file_contents
        
        except KeyboardInterrupt:
            return None

class Logger():
    """
    Standardized handler for error/warning messages

    By default `self.value` is an empty string and 
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

    def __init__(self, value: Any | None = None) -> None:
        self.value = value or ""

    def path_not_found(self, path: str | _os.PathLike | None = None):
        return f"cannot open `{path or self.value}` (No such file or directory)"

    def file_not_found(self, path: str | _os.PathLike | None = None):
        return self.path_not_found(path)

    def permission_denied(self, path: str | _os.PathLike | None = None):
        return f"cannot open `{path or self.value}` (permission denied)"

    def file_exists(self, path: str | _os.PathLike | None = None):
        return f"cannot create directory `{path or self.value}`: File exists"

    def cannot_remove_dir(self, path: str | _os.PathLike | None = None):
        return f"cannot remove `{path or self.value}`: Is a directory"

    def parameter_not_specified(self, param: str | _os.PathLike | None = None):
        return f"{param or self.value} not specified"

    def parameter_not_supported(self, param: str | None = None):
        return f"unsupported option '{param or self.value}'"

    def same_file(self, path1: str | _os.PathLike | None = None, path2: str | _os.PathLike | None = None):
        return f"`{path1 or path2 or self.value}` and `{path2 or path1 or self.value}` are the same file"
