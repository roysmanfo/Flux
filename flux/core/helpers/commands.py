from enum import IntEnum as _IntEnum
import sys as _sys
import os as _os
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from typing import Any, Optional, TextIO, List, Union
from argparse import Namespace as _Namespace

from flux.core.system.privileges import Privileges
from flux.settings.settings import Settings
from flux.core.system.processes import Status
from flux.utils import format as _format
from .arguments import Parser

STATUS_OK = Status.STATUS_OK
STATUS_ERR = Status.STATUS_ERR
STATUS_WARN = Status.STATUS_WARN

class CommandInterface(_ABC):
    """
    Interface class for commands

    Every command that uses is equiped with the standard methods to work on the app.  \n
    Every single command should use this class to keep a consistent standard.

    ### GENERAL ATTRIBUTES
    Attributes shared by commands

    - `IS_PROCESS (const, bool)`        Whether or not the command is being runned as a background thread
    - `sysinfo (variable, Info)`        A reference to the instance of the Info class, containing process information
    - `command (variable, list[str])`   The full command typed by the user (also contains the command name, es. ['ls', 'some_path'])
    - `status (variable, int)`          The return code of the command (default statuses follow the following convention 'STATUS_[err/ok/warn]' )
    - `stdout (variable, TextIO)`       The stdout of the command
    - `stderr (variable, TextIO)`       The stderr of the command
    - `stdin (variable, TextIO)`        The stdin of the command
    - `parser (variable, Parser)`       A program targeted implementation of argparse.ArgumentParser
    - `args (variable, Namespace)`      The usual output returned by ArgumentParser.parse_args
    - `errors (variable, Errors)`       Standardized error/warning messages
    - `colors (variable, Colors)`       Colors for command output, does not have effect outside terminal
    - `levels (variable, Levels)`       All the log levels available
    - `log_level (variable, int)`       Only logs wit higher severity than this number will be displayed (displays everything by default)

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
            try:
                command_instance.fail_safe(e)
                status: int = command_instance.status
            
            except Exception as ex:
                # In case the command also overwites the fail_safe 
                # and the new function contains unhandled exceptions 
                # (why would you modify fail_safe() anyway?)

                # **handle error**
                status = STATUS_ERR

        del command_instance
        return (status if isinstance(status, int) else STATUS_ERR)
        
    ```

    ### LOGGING FUNCTIONS
    These functions work like in the logging module, where only logs with a certain severity are displayed (log_level)

    - `critical()`  This function should be called once a critical error accoures.
    - `fatal()`     This function should be called once a fatal error accoures.
    - `error()`     This function should be called once an error accoures.
    - `warning()`   This function should be called to issue warnings.
    - `info()`      This function should be called for providing the end user with some info.
    - `debug()`     This function should be called for debugging.

    ### HELPER FUNCTIONS
    Other usefull methods, NOT called by the terminal.
    If you want to use these methods you need to call them yourself.
    (print() and printerr() are not affected by the log_level, but are still to output redirection)

    - `input()`                 This is similar to python's `input()`, but uses `self.stdin` and instead of `sys.stdin` .
    - `print()`                 This is similar to python's `print()`, but uses `self.stdout` and instead of `sys.stdout` .
    - `printerr()`              This is similar to `self.print()`, but uses `self.stderr` instead.
    
    ### PROPERTIES
    Other usefull informations about the state of the command

    - `bool` `redirected_stdout()`     True when the stdout has been redirected
    - `bool` `redirected_stderr()`     True when the stderr has been redirected
    - `bool` `redirected_stdin()`      True when the stdin has been redirected
    - `bool` `is_output_red()`         True when the stdout and stderr have been redirected
    - `bool` `is_any_red()`            True when at least one among stdout, stderr and stdin has been redirected
    - `bool` `is_all_red()`            True when stdout, stderr and stdin have been redirected
    - `bool` `is_alive()`              True from when the commaand gets loaded to after exit() or fail_safe()
    - `bool` `has_high_priv()`         True if the command has been run with high/system privileges
    - `bool` `has_sys_priv()`          True if the command has been run with system privileges

    """

    def __init__(self,
                 info: Settings,
                 command: List[str],
                 is_process: bool,
                 stdout: Optional[TextIO] = _sys.stdout,
                 stderr: Optional[TextIO] = _sys.stdout,
                 stdin: Optional[TextIO] = _sys.stdin,
                 privileges: int = Privileges.LOW
                 ) -> None:
        
        self.PRIVILEGES = privileges
        self.IS_PROCESS: bool = is_process
        self.sysinfo: Settings = info
        self.command: List[str] = command
        self.status: Optional[int] = None
        self.stdout = stdout
        self.stderr = stderr
        self.stdin = stdin
        self.parser: Optional[Parser] = None
        self.args: Optional[_Namespace] = None
        self.errors: Errors = Errors()
        self.colors = Colors()

        self.levels = _Levels
        self.log_level = self.levels.NOTSET

        self._is_alive = True



    def __init_subclass__(cls) -> None:
        cls._FLUX_COMMAND = True

    @staticmethod
    def _is_subclass(cls) -> bool:
        cls_mro = [i.__name__ for i in cls.mro()[-3:]]
        self_mro = [i.__name__ for i in CommandInterface.mro()]
        return cls_mro == self_mro

    @staticmethod
    def _is_subclass_instance(instance: object) -> bool:
        if hasattr(instance, "_FLUX_COMMAND"):
            _FLUX_COMMAND = getattr(instance, "_FLUX_COMMAND")
            if type(_FLUX_COMMAND) == bool and _FLUX_COMMAND:
                return True
        return False


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
    @_abstractmethod
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

        if self.redirected_stdout:
            self.stdout.close()
        
        if self.redirected_stderr:
            self.stderr.close()

        if self.redirected_stdin:
            self.stdin.close()



    def exit(self):
        """
        This is the last function that gets called.\n
        This function should be used to define what status code to return
        """
        self._is_alive = False
        return self.status if self.status else STATUS_OK

    def fail_safe(self, exception: Exception):
        """
        This function gets called to capture unhandled exception.\n
        This function may be called at any time, and once called command execution will be terminated without
        `self.close()` or `self.exit()`

        By default creates a crash report as a temp file for the user to see with all the Traceback informations
        and sets `self.status` to `STATUS_ERR`
        """
        from flux.utils.crash_handler import write_error_log
        prefx = self.parser.prog if self.parser else self.command[0] if self.command else ""
        prefx += '_'
        
        if prefx == '_':
            prefx = None
        
        tmp = write_error_log(prefx)[1]

        self.printerr(f"An error accoured while trying to execute command  ({type(exception).__name__})")
        self.printerr(f"The full error log can be found here: \n{tmp}\n")
        self.status = STATUS_ERR

        # close possibly open files
        if self.redirected_stdout:
            self.stdout.close()
        
        if self.redirected_stderr:
            self.stderr.close()

        if self.redirected_stdin:
            self.stdin.close()

        self._is_alive = False

    """
    LOGGING FUNCTIONS
    """
    
    def critical(self, msg: Optional[str] = None, use_color: bool = False):
        """
        This function should be called once a critical error accoures.\n
        This function should be called to handle errors.

        Also sets the status to STATUS_ERR.
        """
        if self.log_level <= _Levels.CRITICAL:
            if use_color:
                self.printerr(f"{self.colors.Fore.RED}{self.parser.prog}: {msg}{self.colors.Fore.RESET}\n")
            else:
                self.printerr(f"{self.parser.prog}: {msg}\n")
        self.status = STATUS_ERR

    def fatal(self, msg: Optional[str] = None, use_color: bool = False):
        """
        This function should be called once a fatal error accoures.\n
        This function should be called to handle errors.

        Also sets the status to STATUS_ERR.
        """
        if self.log_level <= _Levels.FATAL:
            if use_color:
                self.printerr(f"{self.colors.Fore.RED}{self.parser.prog}: {msg}{self.colors.Fore.RESET}\n")
            else:
                self.printerr(f"{self.parser.prog}: {msg}\n")
        self.status = STATUS_ERR

    def error(self, msg: Optional[str] = None, use_color: bool = False):
        """
        This function should be called once an error accoures.\n
        This function should be called to handle errors.

        Also sets the status to STATUS_ERR.
        """
        if self.log_level <= _Levels.ERROR:
            if use_color:
                self.printerr(f"{self.colors.Fore.RED}{self.parser.prog}: {msg}{self.colors.Fore.RESET}\n")
            else:
                self.printerr(f"{self.parser.prog}: {msg}\n")
        self.status = STATUS_ERR

    def warning(self, msg: Optional[str] = None, use_color: bool = False, to_stdout: bool = True):
        """
        This function should be called to issue warnings.\n
        This function should be called to handle warnings (by default writes to stdout).

        Also sets the status to STATUS_WARN.
        """
        if self.log_level <= _Levels.WARNING:
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

        self.status = STATUS_WARN

    def info(self, msg: Optional[str] = None):
        """
        This function should be called for providing the end user with some info.
        """
        if self.log_level <= self.levels.INFO:
            self.print(msg)
    
    def debug(self, msg: Optional[str] = None):
        """
        This function should be called for debugging.
        """
        if self.log_level <= _Levels.DEBUG:
            self.print(msg)

    """
    HELPER FUNCIONS
    """

    def input(self, __prompt: object = "") -> Optional[str]:
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
        
    def print(self, *values: object, sep: Optional[str] = " ", end: Optional[str] = "\n", file: Optional[TextIO] = None,  flush: bool = False) -> None :
        """
        Prints the values to self.stdout.

        - #### sep
        \tstring inserted between values, default a space.

        - #### end
        \tstring appended after the last value, default a newline.
        
        - #### file
        \ta file-like object (stream); defaults to self.stdout
        
        - #### flush
        \twhether to forcibly flush the stream.
        """
        if self.stdout:
            txt = f"{sep}".join([ str(v) for v in values])
            file = self.stdout if file is None else file

            if self.redirected_stdout:
                txt = _format.remove_ansi_escape_sequences(txt)
            
            print(txt, end=end, file=file, flush=flush)

    def printerr(self, *values: object, sep: Optional[str] = " ", end: Optional[str] = "\n", file: Optional[TextIO] = None,  flush: bool = False) -> None :
        """
        Prints the values to self.stderr.

        - #### sep
        \tstring inserted between values, default a space.

        - #### end
        \tstring appended after the last value, default a newline.
        
        - #### file
        \ta file-like object (stream); defaults to self.stderr

        - #### flush
        \twhether to forcibly flush the stream.
        """
        if self.stderr:
            txt = f"{sep}".join([ str(v) for v in values])
            file = self.stderr if file is None else file

            if self.redirected_stderr:
                txt = _format.remove_ansi_escape_sequences(txt)

            print(txt, end=end, file=file, flush=flush)

    @property
    def redirected_stdout(self):
        """
        returns true if the stdout has been redirected
        """
        return not (self.stderr and self.stdout == _sys.stdout)

    @property
    def redirected_stderr(self):
        """
        returns true if the stderr has been redirected
        """
        return not (self.stderr and self.stderr == _sys.stderr)

    @property
    def redirected_stdin(self):
        """
        returns true if the stdin has been redirected
        """
        return not (self.stdin and self.stdin == _sys.stdin)
    
    @property
    def is_output_red(self):
        """
        returns true if the stdout and stderr have been redirected
        """
        return self.redirected_stdout and self.redirected_stderr

    @property
    def is_any_red(self):
        """
        returns true if at least one among stdout, stderr and stdin has been redirected
        """
        return any([self.redirected_stdout, self.redirected_stderr, self.redirected_stdin])

    @property
    def is_all_red(self):
        """
        retuns true if both stdout, stderr and stdin have been redirected
        """
        return all([self.redirected_stdout, self.redirected_stderr, self.redirected_stdin])

    @property
    def is_alive(self):
        """
        retuns true from when the commaand gets loaded to after exit() or fail_safe()
        """
        return self._is_alive
    
    @property
    def has_high_priv(self):
        """
        retuns true if the command has been run with high/system privileges
        """
        return self.PRIVILEGES >= Privileges.HIGH

    @property
    def has_sys_priv(self):
        """
        retuns true if the command has been run with system privileges
        """
        return self.PRIVILEGES >= Privileges.SYSTEM

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

    or by recreating the object in your `setup` 

    ```
    def setup(self):
        super().setup()
        self.errors = Errors(PATH)
    ```

    otherwise you will have to provide the value on each call

    ```
    try:
        # Some operations
    except PermissionError:
        self.error(self.errors.permission_error(PATH))
    ```

    If you define `self.value` and set the parameter to a different value,
    the new parameter will be used instead

    ```
    self.errors.value = 'value1'
    self.error(self.errors.permission_error())         # <- will use 'value1'
    self.error(self.errors.permission_error('value2')) # <- will use 'value2'
    self.error(self.errors.permission_error())         # <- will use 'value1' again
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
    
    def cannot_read_fod(self, path: Optional[Union[str, _os.PathLike]] = None):
        """
        `{path}`: cannot read file or directory
        """
        return f"`{path or self.value}`: cannot read file or directory"
    
    def not_a_dir(self, path: Optional[Union[str, _os.PathLike]] = None):
        """
        `{path}`: Not a directory
        """
        return f"{path or self.value}: Not a directory"

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
    
    def too_many_args(self):
        """
        too many arguments
        """
        return f"too many arguments"

    def same_file(self, path1: Optional[Union[str, _os.PathLike]] = None, path2: Optional[Union[str, _os.PathLike]] = None):
        """
        `{path1}` and `{path2}` are the same file
        """
        return f"`{path1 or path2 or self.value}` and `{path2 or path1 or self.value}` are the same file"

class _Levels(_IntEnum):
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0


class Colors:
    def __init__(self) -> None:
        from . import colors
        self.Fore = colors.Foreground
        self.Back = colors.Background
        self.Style = colors.Styles


