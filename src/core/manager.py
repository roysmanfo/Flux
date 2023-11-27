"""
## Command Manager

This is the place where the input given gets analized and associated
with the respective command (if existent).
"""
import subprocess
import sys
from typing import List, TextIO

from src.settings.info import Info
from .system import loader


def get_stdout(command: List[str]) -> [TextIO, str]:
    if ">>" in command:
        if command.index(">>") < len(command) - 1:
            try:
                pathname = command[command.index(">>") + 1]
                command.remove(">>")
                command.remove(pathname)
                return [open(pathname, "at"), pathname]
            
            except PermissionError:
                return [None, pathname]
            
            except OSError:
                return [None, pathname]
    elif "1>" in command:
        if command.index("1>") < len(command) - 1:
            try:
                pathname = command[command.index("1>") + 1]
                command.remove("1>")
                command.remove(pathname)
                return [open(pathname, "wt"), pathname]
            
            except PermissionError:
                return [None, pathname]
            
            except OSError:
                return [None, pathname]


    return [sys.stdout, None]


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

    if stdout is None:
        print(f"-flux: {out_path}: Permission denied\n")
        return
    

    # Load command
    exec_command_class = loader.load_builtin_script(command_name)
    if not exec_command_class:
        exec_command_class = loader.load_custom_script(command_name)

    if not exec_command_class:
        try:
            # NOTE: In the future also the return code will be saved and used
            p = subprocess.Popen(command_name, stdin=sys.stdin, stdout=stdout, stderr=sys.stderr, text=True)
            is_thread = command[-1] == "&"

            if not is_thread:
                p.wait()
                
        except PermissionError:
            print(f"-flux: {command_name}: unable to run (permission denied)\n")

        except Exception as e:
            print(f"-flux: {command_name}: command not found\n")
                    
        finally:
            return

    try:
        
        is_thread = command[-1] == "&"
        exec_command = exec_command_class(info, command, is_thread, stdout=stdout)

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
