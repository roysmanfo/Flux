"""
## Command Manager

This is the place where the input given gets analized and associated
with the respective command (if existent).
"""
from src.settings.info import Info

from .system import loader

def manage(command: list[str], info: Info) -> None:

    # Match the command name to the corresponding file in ./cmd/
    # for further processing and execution

    from . import helpers

    def execute_command(callable: helpers.commands.CommandInterface) -> None:
        callable.init()
        callable.setup()
        callable.run()
        callable.close()
        callable.exit()

    exec_command: helpers.commands.CommandInterface
    exec_command_class = helpers.commands.CommandInterface

    info.processes.clean()

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


    exec_command_class = loader.load_builtin_script(command_name)
    if not exec_command_class:
        exec_command_class = loader.load_custom_script(command_name)

    if not exec_command_class:
        print(f"-flux: {command_name}: command not found\n")
        return

    try:
        is_thread = command[-1] == "&"
        exec_command = exec_command_class(info, command, is_thread)

        if is_thread:
            command.pop(-1)
            info.processes.add(info, command, exec_command, False)
        else:
            execute_command(exec_command)

    except UnboundLocalError as e:
        if command_name != "":
            print(f"-flux: {command_name}: command not found\n{e}\n")
