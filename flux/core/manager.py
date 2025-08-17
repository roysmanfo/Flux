"""
## Command Manager

This is the place where the input given gets analized and associated
with the respective command (if existent).
"""
import sys
import os
import tempfile
from typing import Iterable, List, Literal, Optional, TextIO, BinaryIO, Union
from pathlib import Path

from flux.core.system.system import System
from flux.core.system import loader
from flux.core.system.interrupts import EventTriggers
from flux.core.helpers.commands import CommandInterface, Status
from flux.utils import parsing
from flux.utils.exceptions import FluxException

# NULL_PATH = os.devnull
NULL_PATH = [
    Path(os.path.join("/", "dev", "null")).resolve(),
    Path(os.devnull).resolve() if os.name != "nt" else Path(os.devnull)
]

def get_stdout(command: List[str], mode: Literal['t', 'b'] = 't') -> Optional[Union[TextIO, BinaryIO]]:
    """
    Returns the stout of the command and pathname of the file if redirection accours 

    :returns stdout: The stdout on which write the output
    """
    
    REDIRECT: str
    MODE: str

    # Append output to file
    if ">>" in command or "&>>" in command:
        REDIRECT = ">>" if ">>" in command else "&>>"
        MODE = "a"
    # Overwite file with output
    elif ">" in command or "1>" in command or "&>" in command :
        REDIRECT = ">" if ">" in command else "1>" if "1>" in command else "&>"
        MODE = "w"

    else:
        return (sys.stdout if mode == 't' else sys.stdout.buffer)

    return _get_stream(command, REDIRECT, MODE + mode)


def get_stderr(command: List[str], mode: Literal['t', 'b'] = 't') -> Optional[Union[TextIO, BinaryIO]]:
    """
    Returns the sterr of the command and pathname of the file if redirection accours 

    :returns stderr: The stderr on which write the output (None if redirected to /dev/null)
    """
    
    REDIRECT: str
    MODE: str

    # Append output to file
    if "&>>" in command:
        REDIRECT = ">>" if ">>" in command else "&>>"
        MODE = "a"
    # Overwite file with output
    elif "2>" in command or "&>" in command:
        REDIRECT = "2>" if "2>" in command else "&>"
        MODE = "w"

    else:
        return (sys.stderr if mode == 't' else sys.stderr.buffer)


    return _get_stream(command, REDIRECT, MODE + mode)


def get_stdin(command: List[str], mode: Literal['t', 'b'] = 't') -> Optional[Union[TextIO, BinaryIO]]:
    """
    Returns the stin of the command and pathname of the file if redirection accours 

    :returns stdin: The stdin on which read the input (None if redirected to /dev/null)
    """

    REDIRECT: str

    if "<<<" in command:
        REDIRECT = "<<<"
    elif "<<" in command:
        REDIRECT = "<<"
    elif "<" in command:
        REDIRECT = "<"
    else:
        return (sys.stdin if mode == 't' else sys.stdin.buffer)

    return _get_stream(command, REDIRECT, "r" + mode)


def _get_stream(command: List[str], redirect: str, mode: str) -> Optional[Union[TextIO, BinaryIO]]:
    if command.index(redirect) < len(command) - 1:
        try:
            pathname = command.pop(command.index(redirect) + 1)
            command.remove(redirect)

            pathname = Path(pathname).resolve()
            
            # create parent dirs if not present
            os.makedirs(pathname.parent, exist_ok=True)
            return open(pathname, mode) if pathname not in NULL_PATH else None
        except PermissionError as e:
            raise PermissionError(f"-flux: {pathname}: Permission denied") from e
    else:
        raise RuntimeError("syntax error near unexpected token `newline`")


def is_output_piped(command: List[str]) -> bool:
    return "|" in command

def delete_used_pipes(pipe_files: Iterable[TextIO]) -> None:
    # NOTE: would be usefull to know in some logs
    #       if one of these is used as pipe (shouldn't happen, but what if ...)
    ignored_files = {sys.stdin.name, sys.stdout.name, sys.stderr.name}
    
    for pipe in pipe_files:
        if pipe.name not in ignored_files:
            try:
                if not pipe.closed:
                    pipe.flush()
                    pipe.close()
                os.remove(pipe.name)
            except:
                # NOTE: again it would be better to know when this appends 
                #       for debug and bug fixing
                pass  
    

def manage(command: List[str], system: System) -> None:

    if not loader.get_search_priority():
        loader.set_search_priority([
            system.settings.syspaths.CMD_BUILTIN_FOLDER,
            system.settings.syspaths.CMD_SCRIPTS_FOLDER,
            system.settings.syspaths.CMD_FPM_FOLDER,
        ])


    commands = parsing.split_commands(command)
    remainning_commands = len(commands)
    num_pipes_left, tot_pipes = 0, 0
    created_pipes: list[TextIO] = []
    pipe = None
    
    # for each comand separated by semicolon
    while remainning_commands > 0:
        command = commands.pop(0)
        piping_detected = is_output_piped(command)

        try:
            if piping_detected:
                num_pipes_left += command.count("|")
                tot_pipes += command.count("|")
                piped_commands = parsing.split_pipe(command)
                commands = piped_commands + commands
                command = commands.pop(0)
                remainning_commands += len(piped_commands) - 1

            exec_command = build(command, system)
            
            if exec_command:
                if num_pipes_left < tot_pipes:
                    exec_command.stdin = pipe
                    exec_command._recv_from_pipe = True

                if num_pipes_left > 0:
                    pipe = create_pipe(system.settings.syspaths.PIPES_FOLDER)
                    created_pipes.append(pipe)
                    exec_command.stdout = pipe
                    exec_command._send_to_pipe = True
                    num_pipes_left -= 1
                
                exec_command._init_pipe()
                if exec_command.IS_PROCESS:
                    command.pop(-1)
                    system.processes.add(system, command, exec_command, False)
                else:
                    status = call(exec_command)
                    if status == Status.STATUS_ERR:
                        system.interrupt_handler.raise_interrupt(EventTriggers.COMMAND_FAILED)
                    elif status in [Status.STATUS_OK, Status.STATUS_WARN]:
                        system.interrupt_handler.raise_interrupt(EventTriggers.COMMAND_EXECUTED)

                    


        except (UnboundLocalError, AssertionError) as e:
            if command[0] != "":
                print(f"-flux: {command[0]}: command not found\n{e}\n", file=sys.stderr)
        finally:
            remainning_commands -= 1
    delete_used_pipes(created_pipes)


def create_pipe(dir_path: str) -> TextIO:
    temp_name = tempfile.mkstemp(prefix="flux_pipe_", dir=dir_path)[1]
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

    # Load command
    try:
        if loader.get_search_priority():
            exec_command_class = loader.load_command(command_name, pass_flux_exceptions=True)
        else:
            exec_command_class = loader.load_builtin_script(command_name)
            if not exec_command_class:
                exec_command_class = loader.load_custom_script(command_name)
    except FluxException as e:
        print(f"-flux: {command_name}: [{e.__class__.__name__}] {e}\n", file=sys.stderr)
        return None


    if not exec_command_class:
        print(f"-flux: {command_name}: command not found\n", file=sys.stderr)
        return None

    if not CommandInterface._is_subclass(exec_command_class):
        print(f"-flux: {command_name}: command not found\n", file=sys.stderr)
        return None

    if not isinstance(exec_command_class.PRELOAD_CONFIGS, loader.PreLoadConfigs):
        print(f"-flux: {command_name}: unable to load command: has incorrectly set loader configurations\n", file=sys.stderr)
        return None

    preload_configs = exec_command_class.PRELOAD_CONFIGS

    # Check for stdout redirect
    try:
        stdin = get_stdin(command, preload_configs.prefered_mode_stdin)
        stdout = get_stdout(command, preload_configs.prefered_mode_stdout)
        stderr = get_stderr(command, preload_configs.prefered_mode_stderr)
    except Exception as e:
        print(f"-flux: {e}\n", file=sys.stderr)
        return None

    # look for piping    
    if stdout is sys.stdout and is_output_piped(command):
        stdout = create_pipe(system.settings.syspaths.PIPES_FOLDER)
    
    is_thread = command[-1].endswith("&") and not command[0].endswith("&")
    exec_command = exec_command_class(system, command, is_thread, stdout=stdout, stderr=stderr, stdin=stdin, privileges=system.privileges.LOW)

    del exec_command_class
    return exec_command

def call(command_instance: CommandInterface) -> Status:
    """
    Execute the loaded script

    :returns status: the command's status code (int)
    :raises AssertionError: if the command_instance isn't an instance of CommandInterface
    """
    assert CommandInterface._is_subclass_instance(command_instance), "argument passed isn't an instance of CommandInterface"

    try:
        command_instance.init()
        command_instance.setup()

        if (command_instance.status == Status.STATUS_ERR or
                (command_instance.parser and command_instance.parser.exit_execution)):

            command_instance.close()
            status = command_instance.exit()
            del command_instance
            return status

        command_instance.run()
        command_instance.close()
        status = command_instance.exit()
        
    except Exception as e:
        command_instance.fail_safe(e)
        status: int = command_instance.status

    del command_instance
    return (status if isinstance(status, int) else Status.STATUS_ERR)

