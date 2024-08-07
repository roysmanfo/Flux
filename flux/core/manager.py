"""
## Command Manager

This is the place where the input given gets analized and associated
with the respective command (if existent).
"""
import sys
import os
import tempfile
from typing import List, Optional, TextIO, Tuple
from pathlib import Path

from flux.core.system.system import System
from flux.core.system import loader
from flux.core.helpers.commands import CommandInterface, STATUS_ERR
from flux.utils import transform

# NULL_PATH = os.devnull
NULL_PATH = [
    Path(os.path.join("/", "dev", "null")).resolve(),
    Path(os.devnull).resolve() if os.name != "nt" else Path(os.devnull)
]

def get_stdout(command: List[str]) -> Tuple[Optional[TextIO], Optional[str]]:
    """
    Returns the stout of the command and pathname of the file if redirection accours 

    :returns
        - The stdout on which write the output
        - the path to that file 

    :rtype Actually returns a list [TextIO | None, str | None]
    """
    
    STD_OUT: List[TextIO, Optional[str]]
    REDIRECT: str
    MODE: str
    pathname = ""


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

            pathname = Path(pathname).resolve()

            STD_OUT = [open(pathname, MODE) if pathname not in NULL_PATH else None, pathname if pathname not in NULL_PATH else None]
        
        except (PermissionError, OSError):
            STD_OUT = [None, pathname]
        
    else:
        raise RuntimeError("syntax error near unexpected token `newline'")

    return STD_OUT


def get_stderr(command: List[str]) -> Tuple[Optional[TextIO], Optional[str]]:
    """
    Returns the sterr of the command and pathname of the file if redirection accours 

    :returns
        - The stderr on which write the output (None if redirected to /dev/null)
        - the path to that file 

    :rtype Actually returns a list [TextIO | None, str | None]
    """
    
    STD_ERR: List[TextIO, Optional[str]]
    REDIRECT: str
    MODE: str
    pathname = ""

    # Append output to file
    if "&>>" in command:
        REDIRECT = ">>" if ">>" in command else "&>>"
        MODE = "at"
    # Overwite file with output
    elif "2>" in command or "&>" in command:
        REDIRECT = "2>" if "2>" in command else "&>"
        MODE = "wt"

    else:
        return [sys.stderr, None]


    if command.index(REDIRECT) < len(command) - 1:
        try:
            pathname = command[command.index(REDIRECT) + 1]
            command.remove(REDIRECT)
            command.remove(pathname)
            
            pathname = Path(pathname).resolve()

            STD_ERR = [open(pathname, MODE) if pathname not in NULL_PATH else None, pathname if pathname not in NULL_PATH else None]
        except (PermissionError, OSError):
            STD_ERR = [None, pathname]
        
    else:
        raise RuntimeError("syntax error near unexpected token `newline'")

    return STD_ERR


def get_stdin(command: List[str]) -> Tuple[Optional[TextIO], Optional[str]]:
    """
    Returns the stin of the command and pathname of the file if redirection accours 

    :returns
        - The stdin on which read the input (None if redirected to /dev/null)
        - the path to that file 

    :rtype Actually returns a list [TextIO | None, str | None]
    """
    
    STD_IN: List[TextIO, Optional[str]]
    REDIRECT: str
    MODE: str = "rt"
    pathname = ""

    if "<<<" in command:
        REDIRECT = "<<<"
    elif "<<" in command:
        REDIRECT = "<<"
    elif "<" in command:
        REDIRECT = "<"
    else:
        return [sys.stdin, None]

    if command.index(REDIRECT) < len(command) - 1:
        try:
            pathname = command[command.index(REDIRECT) + 1]
            command.remove(REDIRECT)
            command.remove(pathname)
            
            pathname = Path(pathname).resolve()

            STD_IN = [open(pathname, MODE) if pathname not in NULL_PATH else None, pathname if pathname not in NULL_PATH else None]
        
        except (PermissionError, OSError):
            STD_IN = [None, pathname]
        
    else:
        raise RuntimeError("syntax error near unexpected token `newline'")

    return STD_IN

def is_output_piped(command: List[str]) -> bool:
    return "|" in command

def manage(command: List[str], system: System) -> None:
    global pipe
    global num_pipes_left


    commands = transform.split_commands(command)
    remainning_commands = len(commands)
    num_pipes_left, tot_pipes = 0, 0
    pipe = None
    
    # for each comand separated by semicolon
    while remainning_commands > 0:
        command = commands.pop(0)
        piping_detected = is_output_piped(command)

        try:
            if piping_detected:
                num_pipes_left += command.count("|")
                tot_pipes += command.count("|")
                piped_commands = transform.split_pipe(command)
                commands = piped_commands + commands
                command = commands.pop(0)
                remainning_commands += len(piped_commands) - 1

            exec_command = build(command, system)
            
            if exec_command:
                if num_pipes_left < tot_pipes:
                    exec_command.stdin = pipe
                    exec_command._recv_from_pipe = True

                if num_pipes_left > 0:
                    pipe = create_pipe()
                    exec_command.stdout = pipe
                    exec_command._send_to_pipe = True
                    num_pipes_left -= 1
                
                exec_command._init_pipe()
                if exec_command.IS_PROCESS:
                    command.pop(-1)
                    system.processes.add(system, command, exec_command, False)
                else:
                    call(exec_command)
           


        except (UnboundLocalError, AssertionError) as e:
            if command[0] != "":
                print(f"-flux: {command[0]}: command not found\n{e}\n", file=sys.stderr)
        finally:
            remainning_commands -= 1


def create_pipe() -> TextIO:
    temp_name = tempfile.mkstemp(prefix="flux_pipe_")[1]
    pipe = open(temp_name, "wt")
    return pipe

def build(command: List[str], system: System) -> Optional[CommandInterface]:
    exec_command: CommandInterface
    exec_command_class = CommandInterface

    # Remove completed Processes
    system.processes.clean()

    # Check for variables
    if system.variables.exists(command[0]):
        command_name = system.variables.get(command[0]).value
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
    try:
        stdout, out_path = get_stdout(command)
        stderr, err_path = get_stderr(command)
        stdin, in_path = get_stdin(command)
    except RuntimeError as e:
        print(f"-flux: {e}\n", file=sys.stderr)
        return None
    
    if stdout is None and out_path is not None:
        print(f"-flux: {out_path}: Permission denied\n", file=sys.stderr)
        return None
    
    if stderr is None and err_path is not None:
        print(f"-flux: {err_path}: Permission denied\n", file=sys.stderr)
        return None
    
    if stdin is None and in_path is not None:
        print(f"-flux: {in_path}: Permission denied\n", file=sys.stderr)
        return None

    # look for piping    
    if stdout is sys.stdout and is_output_piped(command):
        stdout = create_pipe()

    # Load command
    exec_command_class = loader.load_builtin_script(command_name)
    if not exec_command_class:
        exec_command_class = loader.load_custom_script(command_name)

    if not exec_command_class:
        print(f"-flux: {command_name}: command not found\n", file=sys.stderr)
        return None

    if not CommandInterface._is_subclass(exec_command_class):
        print(f"-flux: {command_name}: command not found\n", file=sys.stderr)
        return None
    
    is_thread = command[-1].endswith("&") and not command[0].endswith("&")
    exec_command = exec_command_class(system, command, is_thread, stdout=stdout, stderr=stderr, stdin=stdin, privileges=system.privileges.LOW)

    del exec_command_class
    return exec_command

def call(command_instance: CommandInterface) -> int:
    """
    Execute the loaded script

    `:returns` the command's status code
    `:rtype` int
    `:raises` AssertionError if the command_instance isn't an instance of CommandInterface
    """
    assert CommandInterface._is_subclass_instance(command_instance), "argument passed isn't an instance of CommandInterface"

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

