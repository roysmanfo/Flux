import sys as _sys
import os as _os
from abc import ABC, abstractmethod
from typing import Any, Optional, TextIO, List
from argparse import Namespace

from src.settings.info import Info
from src.core.system.processes import *
from .arguments import Parser

class CommandInterface(ABC):
    """
    Interface class for commands

    Every command that uses is equiped with the standard methods to work on the app.  \n
    Every single command should use this class to keep a consistent standard.

    ### GENERAL ATTRIBUTES
    Attributes shared by commands

    - `IS_PROCESS (const, bool)`        Whether or not the command is being runned as a background thread
    - `info (variable, Info)`           A reference to the instance of the Info class, containing process information
    - `command (variable, list[str])`   The full command typed by the user (also contains the command name, es. ['ls', 'some_path'])
    - `status (variable, int)`          The return code of the command (default statuses follow the following convention 'STATUS_[err/ok/warn]' )
    - `stdout (variable, TextIO)`       The stdout of the command
    - `stderr (variable, TextIO)`       The stderr of the command
    - `stdin (variable, TextIO)`        The stdin of the command
    - `parser (variable, Parser)`       A program targeted implementation of argparse.ArgumentParser
    - `args (variable, Namespace)`      The usual output returned by ArgumentParser.parse_args
    - `errors (variable, Errors)`       Standardized error/warning messages
    - `colors (variable, Colors)`       Colors for command output, does not have effect outside terminal

    ### AUTOMATIC CALLS
    Methods that get called regardless by the terminal

    - `init()`          This function is called on start of execution.
    - `setup()`         This is function is called right before run().
    - `run()`           This is the entry method for the command.
    - `close()`         This is the method that gets called right after run() the command.
    - `exit()`          This is the last method that gets called.
    - `fail_safe()`     This function gets called to capture unhandled exception.

    Execution flow
    ```py

        try:
            command.init()
            command.setup()

            if command.status == STATUS_ERR or command.parser and command.parser.exit_execution:
                command.close()
                status = command.exit()
                return status
            
            command.run()
            command.close()
            status = command.exit()
                
            except Exception as e:
                command.fail_safe(e)
                status: int = command.status

            del command
            return status
    ```

    ### HELPER FUNCTIONS
    Other usefull methods, NOT called by the terminal.
    If you want to use these methods you need to call them yourself.

    - `error()`     This function should be called once an error accoures.
    - `warning()`   This function should be called to issue warnings.
    - `input()`     This is similar to python's `input()`, but uses `self.stdin` and doesn't modify `sys.stdin` .
    - `print()`     This is similar to python's `print()`, but uses `self.stdout` and doesn't modify `sys.stdout` .
    - `printerr()`  This is similar to `self.print()`, but uses `self.stderr` instead.

    """

    def __init__(self,
                 info: Info,
                 command: List[str],
                 is_process: bool,
                 stdout: Optional[TextIO] = _sys.stdout,
                 stderr: Optional[TextIO] = _sys.stdout,
                 stdin: Optional[TextIO] = _sys.stdin
                 ) -> None:

        self.IS_PROCESS: bool = is_process
        self.info: Info = info
        self.command: List[str] = command
        self.status: Optional[int] = None
        self.stdout = stdout
        self.stderr = stderr
        self.stdin = stdin
        self.parser: Optional[Parser] = None
        self.args: Optional[Namespace] = None
        self.errors: Errors = Errors()
        self.colors = Colors(not (stdout is _sys.stdout))

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
                self.status = STATUS_ERR
                print()
                return
        except AttributeError:
            self.args = None
    
    # ! This method MUST be overwritten
    @abstractmethod
    def run(self):
        """
        This is the entry function for the command.\n
        This function should be used to manage arguments and adapt command execution.
        """
        ...

    def close(self):
        """
        This is the function that gets called after we run the command.\n
        This function is used to close open files, like a redirected stdout
        """        

        if self.stdout != _sys.stdout:
            self.stdout.close()



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
        and sets `self.status` to `STATUS_ERR`
        """
        from src.utils.crash_handler import write_error_log
        prefx = self.parser.prog if self.parser else self.command[0]
        prefx += '_'
        
        if prefx == '_':
            prefx = None
        
        tmp = write_error_log(prefx)[1]

        self.printerr(f"An error accoured while trying to execute command  ({type(exception).__name__})")
        self.printerr(f"The full error log can be found here: \n{tmp}\n")
        self.status = STATUS_ERR
        

    """
    HELPER FUNCTIONS
    """
    
    def error(self, msg: Optional[str] = None, use_color: bool = False, status: Optional[int] = None):
        """
        This function should be called once an error accoures.\n
        This function should be called to handle errors.

        By default sets the status to STATUS_ERR.
        """
        if use_color:
            self.printerr(f"{self.colors.Fore.RED}{self.parser.prog}: {msg}{self.colors.Fore.RESET}\n")
        else:
            self.printerr(f"{self.parser.prog}: {msg}\n")
        self.status = status or STATUS_ERR

    def warning(self, msg: Optional[str] = None, status: Optional[int] = None, use_color: bool = False, to_stdout: bool = True):
        """
        This function should be called to issue warnings.\n
        This function should be called to handle warnings (by default writes to stdout).

        By default sets the status to STATUS_WARN.
        """

        if to_stdout:
            if use_color:
                self.print(f"{self.colors.Fore.YELLOW}{self.parser.prog}: {msg}{self.colors.Fore.RESET}")
            else:
                self.print(msg)
        else:
            if use_color:
                self.print(f"{self.colors.Fore.YELLOW}{self.parser.prog}: {msg}{self.colors.Fore.RESET}")
            else:
                self.print(msg)

        self.status = status or STATUS_WARN

    def input(self, __prompt: object = "") -> str | None:
        """
        This function takes an input from the stdin and returns it as a string

        If a Ctrl-c is detected, returns None.
        """
        try:
            if __prompt:
                self.print(__prompt, end="")

            if not self.stdin.readable():
                return None

            file_contents = self.stdin.readline()
            
            if file_contents == '':
                return None
            
            return file_contents
        except KeyboardInterrupt:
            return None
        
    def print(self, *values: object, sep: Optional[str] = " ", end: Optional[str] = "\n",  flush: bool = False) -> None :
        """
        Prints the values to self.stdout.

        - #### sep
        \tstring inserted between values, default a space.

        - #### end
        \tstring appended after the last value, default a newline.

        - #### flush
        \twhether to forcibly flush the stream.
        """
        if self.stdout:
            self.stdout.write(f"{sep}".join([ v.__str__() for v in values]))
            self.stdout.write(end)

            if flush:
                self.stdout.flush()

    def printerr(self, *values: object, sep: Optional[str] = " ", end: Optional[str] = "\n",  flush: bool = False) -> None :
        """
        Prints the values to self.stderr.

        - #### sep
        \tstring inserted between values, default a space.

        - #### end
        \tstring appended after the last value, default a newline.

        - #### flush
        \twhether to forcibly flush the stream.
        """
        if self.stderr:
            self.stderr.write(f"{sep}".join([ v.__str__() for v in values]))
            self.stderr.write(end)

            if flush:
                self.stdout.flush()
        




class Errors():
    """
    Standardized error/warning messages

    By default `self.value` is an empty string and 
    will be used if no value is given as function argument,

    You can change its value in the `run` function

    ```
    def run(self):    
        self.errors.value = self.args.PATH
    ```

    or by recreating the object in your setup 

    ```
    def setup(self):
        super().setup()
        self.errors = Errors(PATH)
    ```

    otherwise you will have to provide the path on each call

    ```
    try:
        # Some operations
    except PermissionError:
        self.error(self.errors.permission_error(PATH))
    ```
    """

    def __init__(self, value: Optional[Any] = None) -> None:
        self.value = value or ""

    def path_not_found(self, path: Optional[Union[str, _os.PathLike]] = None):
        """
        cannot open `{path}` (No such file or directory)
        """
        return f"cannot open `{path or self.value}` (No such file or directory)"

    def file_not_found(self, path: Optional[Union[str, _os.PathLike]] = None):
        """
        cannot open `{path}` (No such file or directory)
        """
        return self.path_not_found(path)

    def permission_denied(self, path: Optional[Union[str, _os.PathLike]] = None):
        """
        cannot open `{path}` (permission denied)
        """
        return f"cannot open `{path or self.value}` (permission denied)"

    def file_exists(self, path: Optional[Union[str, _os.PathLike]] = None):
        """
        cannot create directory `{path}`: File exists
        """
        return f"cannot create directory `{path or self.value}`: File exists"

    def cannot_remove_dir(self, path: Optional[Union[str, _os.PathLike]] = None):
        """
        cannot remove `{path}`: Is a directory
        """
        return f"cannot remove `{path or self.value}`: Is a directory"

    def cannot_read_dir(self, path: Optional[Union[str, _os.PathLike]] = None):
        """
        cannot read `{path}`: Is a directory
        """
        return f"cannot read `{path or self.value}`: Is a directory"

    def parameter_not_specified(self, param: Optional[Union[str, _os.PathLike]] = None):
        """
        `{param}` not specified
        """
        return f"{param or self.value} not specified"

    def parameter_not_supported(self, param: Optional[str] = None):
        """
        unsupported option `{param}`
        """
        return f"unsupported option '{param or self.value}'"

    def invalid_argument(self, param: Optional[str] = None, rule: Optional[str] = None):
        """
        invalid argument `{param}`: `{rule}`

        invalid argument `{param}`
        """

        if rule:
            return f"invalid argument '{param or self.value}': {rule}"

        return f"invalid argument '{param or self.value}'"

    def same_file(self, path1: Optional[Union[str, _os.PathLike]] = None, path2: Optional[Union[str, _os.PathLike]] = None):
        """
        `{path1}` and `{path2}` are the same file
        """
        return f"`{path1 or path2 or self.value}` and `{path2 or path1 or self.value}` are the same file"


class Colors:
    def __init__(self, to_file: bool) -> None:
        from . import colors
        self.Fore = colors.Foreground(to_file)
        self.Back = colors.Background(to_file)
        self.Style = colors.Styles(to_file)

