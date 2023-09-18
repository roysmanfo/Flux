"""
## Command Manager

This is the place where the input given gets analized and associated
with the respective command (if existent).
"""
from src.settings.info import Info
import os
import importlib

# List of directories to search for custom scripts/extensions
custom_script_dirs = ["scripts", "extensions"]


def load_custom_script(script_name: str):
    """
    Load an external command installed on the machine
    """

    for dir_name in custom_script_dirs:
        script_path = os.path.join(dir_name, script_name + ".py")
        if os.path.isfile(script_path):
            try:
                module = importlib.import_module(f"{dir_name}.{script_name}")
                exec_command_class = getattr(module, "Command")
                return exec_command_class
            except (ImportError, AttributeError):
                pass
    return None


def manage(command: list[str], info: Info) -> None:

    # Match the command name to the corresponding file in ./cmd/
    # for further processing and execution

    from . import cmd as fluxcmd
    from . import helpers

    def execute_command(callable: helpers.commands.CommandInterface, command) -> None:
        callable.init()
        callable.run(command)
        callable.close()
        callable.exit()

    exec_command: helpers.commands.CommandInterface
    exec_command_class = helpers.commands.CommandInterface

    info.processes.clean()

    if info.variables.exists(command[0]):
        command_name = info.variables.get(command[0]).value
    else:
        command_name = command[0]

    if command[0].startswith("$"):
        command.pop(0)
        tail = command
        command = command_name.split()
        command.extend(tail)
        command_name = command[0]


    match command_name:
        case "":            return
        case "export":      exec_command_class = fluxcmd.export.Command
        case "file":        exec_command_class = fluxcmd.file.Command
        case "flux":        exec_command_class = fluxcmd.flux.Command
        case "fpm":         exec_command_class = fluxcmd.fpm.Command
        case "joke":        exec_command_class = fluxcmd.joke.Command
        case "ls":          exec_command_class = fluxcmd.ls.Command
        case "observer":    exec_command_class = fluxcmd.observer.Command
        case "ps":          exec_command_class = fluxcmd.ps.Command
        case "rm":          exec_command_class = fluxcmd.rm.Command
        case "systemctl":   exec_command_class = fluxcmd.systemctl.Command
        case "zip":         exec_command_class = fluxcmd.zip.Command
        case "unzip":       exec_command_class = fluxcmd.unzip.Command
        case _:             exec_command_class = load_custom_script(command_name)

        


    if not exec_command_class:
        print(f"-flux: {command_name}: command not found\n")
        return

    try:
        is_thread = command[-1] == "&"
        exec_command = exec_command_class(info, is_thread)

        if is_thread:
            command.pop(-1)
            info.processes.add(info, command, exec_command, False)
        else:
            execute_command(exec_command, command)

    except UnboundLocalError as e:
        if command_name != "":
            print(f"-flux: {command_name}: command not found\n{e}\n")
