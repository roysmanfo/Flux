"""
## Command Manager

This is the place where the input given gets analized and associated
with the respective command (if existent).
"""
from src.settings.info import Info

def manage(command: list[str], info: Info) -> None:

    # Match the command name to the corresponding file in ./cmd/
    # for further processing and execution

    from . import cmd as fluxcmd

    def execute_command(callable: fluxcmd.helpers.commands.CommandInterface, command) -> None:
        callable.init()
        callable.run(command)
        callable.close()
        callable.exit()

    exec_command: fluxcmd.helpers.commands.CommandInterface
    exec_command_class = fluxcmd.helpers.commands.CommandInterface

    info.processes.clean()

    if command[0] == "export":
        exec_command_class = fluxcmd.export.Command

    elif command[0] == "flux":
        exec_command_class = fluxcmd.flux.Command

    elif command[0] == "joke":
        exec_command_class = fluxcmd.joke.Command
    
    elif command[0] == "ls":
        exec_command_class = fluxcmd.ls.Command
    
    elif command[0] == "observer":
        exec_command_class = fluxcmd.observer.Command

    elif command[0] == "set":
        exec_command_class = fluxcmd.set.Commmand

    try:
        is_thread = command[-1] == "&"
        exec_command = exec_command_class(info, is_thread)

        if is_thread:
            from threading import Thread
            command.pop(-1)
            thread = Thread(target=execute_command, args=(
                exec_command, command), name=command[0])
            info.processes.add(info, thread)
        else:
            execute_command(exec_command, command)

    except UnboundLocalError as e:
        if command[0] != "":
            print(f"-flux: {command[0]}: command not found\n{e}\n")


