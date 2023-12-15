"""
## Command Manager

This is the place where the input given gets analized and associated
with the respective command (if existent).
"""
import sys
from typing import List, Optional, TextIO, Tuple

from src.settings.info import Info
from .system import loader


def get_stdout(command: List[str]) -> Tuple[TextIO, Optional[str]]:
    """
    Returns the stout of the command and pathname of the file if redirection accours 

    :returns
        - The stdout on which write the output
        - the path to that file 

    :rtype Actually returns a list [TextIO, str | None]
    """
    
    SOUT: list[TextIO, Optional[str]]
    REDIRECT: str
    MODE: str


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
            SOUT = [open(pathname, MODE), pathname]
        
        except PermissionError:
            SOUT = [None, pathname]
        
        except OSError:
            SOUT = [None, pathname]

    return SOUT


def get_stderr(command: List[str]) -> Tuple[TextIO, Optional[str]]:
    """
    Returns the sterr of the command and pathname of the file if redirection accours 

    :returns
        - The stderr on which write the output (None if redirected to /dev/null)
        - the path to that file 

    :rtype Actually returns a list [TextIO, str | None]
    """
    
    SOUT: list[TextIO, Optional[str]]
    REDIRECT: str
    MODE: str


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
            
            SOUT = [open(pathname, MODE), pathname]
        
        except PermissionError:
            SOUT = [None, pathname]
        
        except OSError:
            SOUT = [None, pathname]
    else:
        SOUT = [None, pathname]

    return SOUT

def manage(command: List[str], info: Info) -> None:

    # Match the command name to the corresponding file in ./cmd/
    # for further processing and execution

    from . import helpers

    def execute_script(callable: helpers.commands.CommandInterface) -> int:
        """
        Execute the loaded script

        `:returns` the command's status code\n
        `:rtype` int
        """
        try:
            callable.init()
            callable.setup()

            if callable.parser and callable.parser.exit_execution:
                callable.close()
                status = callable.exit()
                return status
            
            callable.run()
            callable.close()
            status = callable.exit()
            
        except Exception as e:
            callable.fail_safe(e)
            status: int = callable.status

        del callable
        return status

    exec_command: helpers.commands.CommandInterface
    exec_command_class = helpers.commands.CommandInterface

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

    if stdout is None:
        print(f"-flux: {out_path}: Permission denied\n")
        return
    
    if stderr is None:
        print(f"-flux: {err_path}: Permission denied\n")
        return
    

    # Load command
    exec_command_class = loader.load_builtin_script(command_name)
    if not exec_command_class:
        exec_command_class = loader.load_custom_script(command_name)

    if not exec_command_class:
        print(f"-flux: {command_name}: command not found\n")
        return

    try:
        
        is_thread = command[-1] == "&"
        exec_command = exec_command_class(info, command, is_thread, stdout=stdout, stderr=stderr)

        if is_thread:
            command.pop(-1)
            info.processes.add(info, command, exec_command, False)
        else:
            execute_script(exec_command)
            

    except UnboundLocalError as e:
        if command_name != "":
            print(f"-flux: {command_name}: command not found\n{e}\n")

    finally:
        del exec_command_class
