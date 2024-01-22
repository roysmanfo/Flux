"""
## Command Manager

This is the place where the input given gets analized and associated
with the respective command (if existent).
"""
import sys
import os
from typing import List, Optional, TextIO, Tuple

from src.settings.info import Info
from .system import loader
from .helpers.commands import CommandInterface, STATUS_ERR

NULL_PATH = os.devnull

def get_stdout(command: List[str]) -> Tuple[Optional[TextIO], Optional[str]]:
    """
    Returns the stout of the command and pathname of the file if redirection accours 

    :returns
        - The stdout on which write the output
        - the path to that file 

    :rtype Actually returns a list [TextIO | None, str | None]
    """
    
    STD_OUT: list[TextIO, Optional[str]]
    REDIRECT: str
    MODE: str
    pathname = None


    # Append output to file
    if ">>" in command or "&>>" in command:
        REDIRECT = ">>" if ">>" in command else "&>>"
        MODE = "at"
    # Overwite file with output
    elif ">" in command or "1>" in command or "&>" in command :
        REDIRECT = ">" if ">" in command else "1>" if "1>" in command else "&>"
        MODE = "wt"

    else:
        return [sys.stdout, None]


    if command.index(REDIRECT) < len(command) - 1:
        try:
            pathname = command[command.index(REDIRECT) + 1]
            command.remove(REDIRECT)
            command.remove(pathname)
            STD_OUT = [open(pathname, MODE) if pathname != NULL_PATH else None, pathname if pathname != NULL_PATH else None]
        
        except (PermissionError, OSError):
            STD_OUT = [None, pathname]
        
    else:
        STD_OUT = [None, pathname]

    return STD_OUT


def get_stderr(command: List[str]) -> Tuple[Optional[TextIO], Optional[str]]:
    """
    Returns the sterr of the command and pathname of the file if redirection accours 

    :returns
        - The stderr on which write the output (None if redirected to /dev/null)
        - the path to that file 

    :rtype Actually returns a list [TextIO | None, str | None]
    """
    
    STD_ERR: list[TextIO, Optional[str]]
    REDIRECT: str
    MODE: str
    pathname = None

    # Append output to file
    if "&>>" in command:
        REDIRECT = ">>" if ">>" in command else "&>>"
        MODE = "at"
    # Overwite file with output
    elif "2>" in command or "&>" in command:
        REDIRECT = "2>" if "2>" in command else "&>"
        MODE = "wt"

    else:
        return [sys.stdout, None]


    if command.index(REDIRECT) < len(command) - 1:
        try:
            pathname = command[command.index(REDIRECT) + 1]
            command.remove(REDIRECT)
            command.remove(pathname)
            
            STD_ERR = [open(pathname, MODE) if pathname != NULL_PATH else None, pathname if pathname != NULL_PATH else None]
        
        except (PermissionError, OSError):
            STD_ERR = [None, pathname]
        
    else:
        STD_ERR = [None, pathname]

    return STD_ERR


def get_stdin(command: List[str]) -> Tuple[Optional[TextIO], Optional[str]]:
    """
    Returns the stin of the command and pathname of the file if redirection accours 

    :returns
        - The stdin on which read the inut (None if redirected to /dev/null)
        - the path to that file 

    :rtype Actually returns a list [TextIO | None, str | None]
    """
    
    STD_IN: list[TextIO, Optional[str]]
    REDIRECT: str
    MODE: str
    pathname = None

    if "<" in command:
        REDIRECT = "<"
        MODE = "rt"
    else:
        return [sys.stdout, None]


    if command.index(REDIRECT) < len(command) - 1:
        try:
            pathname = command[command.index(REDIRECT) + 1]
            command.remove(REDIRECT)
            command.remove(pathname)
            
            STD_IN = [open(pathname, MODE) if pathname != NULL_PATH else None, pathname if pathname != NULL_PATH else None]
        
        except (PermissionError, OSError):
            STD_IN = [None, pathname]
        
    else:
        STD_IN = [None, pathname]

    return STD_IN



def manage(command: List[str], info: Info) -> None:        
    try:
        exec_command = build(command, info)

        if exec_command.IS_PROCESS:
            command.pop(-1)
            info.processes.add(info, command, exec_command, False)
        else:
            call(exec_command)
    
    except UnboundLocalError as e:
        if command[0] != "":
            print(f"-flux: {command[0]}: command not found\n{e}\n")


def build(command: List[str], info: Info) -> CommandInterface | None:
    exec_command: CommandInterface
    exec_command_class = CommandInterface

    # Remove completed Processes
    info.processes.clean()

    # Check for variables
    if info.variables.exists(command[0]):
        command_name = info.variables.get(command[0]).value
    else:
        command_name = command[0]

    command_name = str(command_name)

    if command[0].startswith("$"):
        command.pop(0)
        tail = command
        command = command_name.split()
        command.extend(tail)
        command_name = command[0]


    # Check for stdout redirect
    stdout, out_path = get_stdout(command)
    stderr, err_path = get_stderr(command)
    stdin, in_path = get_stdin(command)

    if stdout is None:
        print(f"-flux: {out_path}: Permission denied\n")
        return None
    
    if stderr is None:
        print(f"-flux: {err_path}: Permission denied\n")
        return None
    
    if stdin is None:
        print(f"-flux: {in_path}: Permission denied\n")
        return None
    

    # Load command
    exec_command_class = loader.load_builtin_script(command_name)
    if not exec_command_class:
        exec_command_class = loader.load_custom_script(command_name)

    if not exec_command_class:
        print(f"-flux: {command_name}: command not found\n")
        return None
    
    is_thread = command[-1].endswith("&") and not command[0].endswith("&")
    # XXX: Ensure stability on python 3.12 as threads created by flux are not supported (#44)
    is_thread = is_thread and sys.version_info < (3, 12)
    exec_command = exec_command_class(info, command, is_thread, stdout=stdout, stderr=stderr, stdin=stdin)

    if not isinstance(exec_command, CommandInterface):
        return None
    del exec_command_class
    return exec_command

def call(command_instance: CommandInterface) -> int:
    """
    Execute the loaded script

    `:returns` the command's status code
    `:rtype` int
    `:raises` ValueError if the command_instance isn't an instance of CommandInterface
    """

    assert isinstance(command_instance, CommandInterface), ValueError("argument passed isn't an instance of CommandInterface")

    try:
        command_instance.init()
        command_instance.setup()

        if command_instance.status == STATUS_ERR or command_instance.parser and command_instance.parser.exit_execution:
            command_instance.close()
            return command_instance.exit()
        
        command_instance.run()
        command_instance.close()
        status = command_instance.exit()
        
    except Exception as e:
        command_instance.fail_safe(e)
        status: int = command_instance.status

    del command_instance
    return (status if isinstance(status, int) else STATUS_ERR)

