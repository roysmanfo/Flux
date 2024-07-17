import sys as _sys
import os as _os
from enum import IntEnum as _IntEnum
from argparse import Namespace as _Namespace
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from typing import Any, Callable, Mapping, Optional, TextIO, List, Tuple, Union

from flux.core.system.interrupts import EventTriggers, IHandle
from flux.core.system.privileges import Privileges
from flux.core.system.processes import Status
from flux.core.system.system import System
from flux.settings.settings import Settings
from flux.utils import format as _format
from .arguments import Parser

STATUS_OK = Status.STATUS_OK
STATUS_ERR = Status.STATUS_ERR
STATUS_WARN = Status.STATUS_WARN

class _Levels(_IntEnum): ...

class CommandInterface(_ABC):
    """
    Interface class for commands

    Every command that uses is equiped with the standard methods to work on the app.  \n
    Every single command should use this class to keep a consistent standard.

    ### GENERAL ATTRIBUTES
    Attributes shared by commands

    - `IS_PROCESS (const, bool)`        Whether or not the command is being runned as a background thread
    - `PRIVILEGES (const, Privileges)`  The privileges given to the user to execute the current command [LOW / HIGH / SYSTEM]
    - `system (variable, System)`       A reference to the instance of the System class, containing all the most important informations about flux
    - `settings (variable, Settings)`   A reference to the instance of the Settings class, containing user settings and system paths (SysPaths)
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
    - `run()`           This is the core method for the command.
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
            command_instance.fail_safe(e)
            status: int = command_instance.status

        del command_instance
        return (status if isinstance(status, int) else STATUS_ERR)
        
    ```

    ### LOGGING METHODS
    These methods work like in the logging module, where only logs with a certain severity are displayed (log_level)

    - `critical()`  This mathod should be called once a critical error accoures.
    - `fatal()`     This mathod should be called once a fatal error accoures.
    - `error()`     This mathod should be called once an error accoures.
    - `warning()`   This mathod should be called to issue warnings.
    - `info()`      This mathod should be called for providing the end user with some info.
    - `debug()`     This mathod should be called for debugging.

    ### HELPER METHODS
    Other usefull methods, NOT called by the terminal.
    If you want to use these methods you need to call them yourself.
    (print() and printerr() are not affected by the log_level, but are still to output redirection)

    - `input()`                 This is similar to python's `input()`, but uses `self.stdin` and instead of `sys.stdin` .
    - `print()`                 This is similar to python's `print()`, but uses `self.stdout` and instead of `sys.stdout` .
    - `printerr()`              This is similar to `self.print()`, but uses `self.stderr` instead.
    - `get_level_name()`        Returns the level's name based on value
    - `get_level_val()`         Returns the level's value based on it's name    
    - `register_interrupt()`    Register a new interrupt handler
    - `unregister_interrupt()`  Unregister an interrupt handler
    - `clear_interrupts()`      Unregisters all interrupts
    
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
    - `bool` `ihandles()`              Retuns a set of all interrupt handles
    - `bool` `recv_from_pipe()`        True if `self.stdin` is pointing to a `pipe`
    - `bool` `send_to_pipe()`          True if `self.stdout` is pointing to a `pipe`

    """
    def __init__(self,
                 system: System,
                 command: List[str],
                 is_process: bool,
                 stdout: Optional[TextIO] = _sys.stdout,
                 stderr: Optional[TextIO] = _sys.stdout,
                 stdin: Optional[TextIO] = _sys.stdin,
                 privileges: Privileges = Privileges.LOW
                 ) -> None:
        
        self.PRIVILEGES = privileges
        self.IS_PROCESS: bool = is_process
        self.system: System = system
        self.settings: Settings = self.system.settings
        self.command: List[str] = command
        self.status: Optional[Status] = None
        self.stdout = stdout
        self.stderr = stderr
        self.stdin = stdin
        self.parser: Optional[Parser] = None
        self.args: Optional[_Namespace] = None
        self.errors: Errors = Errors()
        self.colors = Colors()
        self.levels = _Levels
        self.log_level = self.levels.NOTSET

        self._recv_from_pipe = False
        self._send_to_pipe = False
        self._is_alive = True
        self._stored_ihandles: set[IHandle] = set()    

    def _init_pipe(self) -> None:
        if self.recv_from_pipe:
            self.stdin = open(self.stdin.name, "r")

    def __new__(cls, *args, **kwargs):
        # override of these methods is not allowed
        NAMES = {"__init__", "__new__", "fail_safe"}

        instance = super().__new__(cls)
        for name, method in cls.__dict__.items():
            if callable(method) and name in NAMES:
                if hasattr(CommandInterface, name) and getattr(CommandInterface, name) is not method:
                    raise RuntimeError(f"Method '{name}' can't be overrided in subclass.")
        return instance

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

    def init(self) -> None:
        """
        This method is called on start of execution.\n
        This method should be used to do setup operations (like create the Parser)
        """
        ...

    def setup(self) -> None:
        """
        This is method is called right before run().\n
        This method is used to parse arguments and exit on parsing errors

        NOTE: Always remember to call `super().setup()` when overwriting this method
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
    def run(self) -> None:
        """
        This is the core method for the command.\n
        This method should be used to do all the main operations of the command.

        NOTE: If this method has not been implemented, the command will NOT be executed.
        """
        ...

    def close(self) -> None:
        """
        This is the method that gets called after we run the command.\n
        This method is used to close open files, like a redirected stdout

        NOTE: Always remember to call `super().close()` when overwriting this method
        """        

        if self.stdout and self.redirected_stdout:
            self.stdout.close()
        
        if self.stderr and self.redirected_stderr:
            self.stderr.close()

        if self.stdin and self.redirected_stdin:
            self.stdin.close()

        self.clear_interrupts(force=True)


    def exit(self) -> Status:
        """
        This is the last method that gets called.\n
        This method should be used to define what status code to return

        NOTE: Always remember to call `super().exit()` when overwriting this method
        """
        self._is_alive = False
        return self.status if self.status else STATUS_OK

    def fail_safe(self, exception: Exception) -> None:
        """
        This method gets called to capture unhandled exception.\n
        This method may be called at any time, and once called command execution will be terminated without
        calling `self.close()` or `self.exit()`

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
        if self.stdout and self.redirected_stdout:
            self.stdout.close()
        
        if self.stderr and self.redirected_stderr:
            self.stderr.close()

        if self.stdin and self.redirected_stdin:
            self.stdin.close()

        self._is_alive = False
        self.clear_interrupts(force=True)

    """
    LOGGING METHODS
    """
    
    def critical(self, msg: Optional[str] = None, use_color: bool = False):
        """
        This method should be called once a critical error accoures.\n
        This method should be called to handle errors.

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
        This method should be called once a fatal error accoures.\n
        This method should be called to handle errors.

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
        This method should be called once an error accoures.\n
        This method should be called to handle errors.

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
        This method should be called to issue warnings.\n
        This method should be called to handle warnings (by default writes to stdout).

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
        This method should be called for providing the end user with some info.
        """
        if self.log_level <= self.levels.INFO:
            self.print(msg)
    
    def debug(self, msg: Optional[str] = None):
        """
        This method should be called for debugging.
        """
        if self.log_level <= _Levels.DEBUG:
            self.print(msg)

    """
    HELPER METHODS
    """

    def input(self, __prompt: object = "") -> Optional[str]:
        """
        This method takes an input from the stdin and returns it as a string

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
            txt = f"{sep}".join([ str(v) for v in values if v])
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
            txt = f"{sep}".join([ str(v) for v in values if v])
            file = self.stderr if file is None else file

            if self.redirected_stderr:
                txt = _format.remove_ansi_escape_sequences(txt)

            print(txt, end=end, file=file, flush=flush)

    @property
    def redirected_stdout(self):
        """
        returns true if the stdout has been redirected
        """
        return not (self.stdout and self.stdout == _sys.stdout)

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

    @property
    def ihandles(self):
        """
        retuns a set of all interrupt handles
        """
        return self._stored_ihandles

    @property
    def recv_from_pipe(self):
        """
        returns true if `self.stdin` is pointing to a `pipe`
        """
        return self._recv_from_pipe
    
    @property
    def send_to_pipe(self):
        """
        returns true if `self.stdout` is pointing to a `pipe`
        """
        return self._send_to_pipe

    def get_level_name(self, level_val: _Levels) -> Optional[str]:
        """
        returns the level's name based on value
        """
        return _lvl_val_to_name.get(level_val, None)

    def get_level_val(self, level_name: str) -> Optional[_Levels]:
        """
        returns the level's value based on it's name
        """
        return _lvl_name_to_val.get(level_name, None)
    
    def clear_interrupts(self, force: bool = True) -> None:
        """
        Unregisters all interrupts

        `:param force` when set to false the interrupt will be removed only if it has been executed at least once
        """
        ihandles = [i for i in self._stored_ihandles]
        for h in ihandles:
            self.unregister_interrupt(h, force=force)

    def register_interrupt(self,
                         event: EventTriggers,
                         target: Callable[[Any], None],
                         args: Optional[Tuple[Any]]= (),
                         kwargs: Optional[Mapping[str, Any]] = None,
                         exec_once: Optional[bool] = True) -> IHandle:
        """
        Register a new interrupt handler

        :param event: can be one of the supported Signals or EventTriggers. Specifies when to execute the interrupt
        :param target: the actual code to execute once the specified event occours
        :param args: the arguments needed by the target function
        :param kwargs: is a dictionary of keyword arguments for the target invocation. Defaults to {}.
        :param exec_once: if set to False, the interrupt will be executed at each event, as long as the command is still alive
        :returns an handle to the Interrupt, which will be useful when interacting with it
        """
        ihandle = self.system.interrupt_handler._register(event, target, args, kwargs, exec_once)
        self._stored_ihandles.add(ihandle)
        return ihandle
    

    def unregister_interrupt(self, handle: IHandle, force: bool = False) -> bool:
        """
        Unregister an interrupt handler

        :param handle: an handle to the Interrupt to remove
        :param force: if True, the interrupt will be removed even if it hasn't been executed yet
        :returns True if the interrupt has been removed, or has not been found, False otherwise
        """
        res = self.system.interrupt_handler._unregister(handle, force)

        if res:
            self._stored_ihandles.discard(handle)
        return res

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

_lvl_name_to_val = {
    "CRITICAL": _Levels.CRITICAL,
    "FATAL": _Levels.FATAL,
    "ERROR": _Levels.ERROR,
    "WARNING": _Levels.WARNING,
    "WARN": _Levels.WARN,
    "INFO": _Levels.INFO,
    "DEBUG": _Levels.DEBUG,
    "NOTSET": _Levels.NOTSET,
}

_lvl_val_to_name = {
    _Levels.CRITICAL: "CRITICAL",
    _Levels.FATAL: "FATAL",
    _Levels.ERROR: "ERROR",
    _Levels.WARNING: "WARNING",
    _Levels.WARN: "WARN",
    _Levels.INFO: "INFO",
    _Levels.DEBUG: "DEBUG",
    _Levels.NOTSET: "NOTSET",
}

class Colors:
    def __init__(self) -> None:
        from . import colors
        self.Fore = colors.Foreground
        self.Back = colors.Background
        self.Style = colors.Styles


