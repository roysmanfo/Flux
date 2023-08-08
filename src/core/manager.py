"""
## Command Manager

This is the place where the input given gets analized and associated
with the respective command (if existent).
"""


def classify_arguments(command: list) -> dict:
    """
    Classifies the arguments of to the command in a dictionary,
    divideing each argument in 3 sections:
     - command :    a string containing the actual command given
     - flags :      a list of allthe flags that modify how the command is executed (es. -n 3)
     - variables :  a list of vareables that a flag might require
     - options :    a list of all the options that modify what the command does

    #### Example
        input:  ["sortfiles", "/reverse"]

        output: {"command": "sortfiles", "flags": [], "variables": [], "options":["/reverse"]}
    """

    classified = {"command": "", "flags": [], "variables": [], "options": []}

    options, flags, variables = [], [], []

    for i in command:
        if command[0] == i:
            continue
        if i[0] == "/":
            options.append(i)
        elif i[0] == "-":
            flags.append(i)
        else:
            variables.append(i)

    classified["command"] = command[0].lower()
    classified["flags"] = flags
    classified["variables"] = variables
    classified["options"] = options

    return classified


def manage(cmd: list[str], info: object) -> None:

    # Classify command line arguments and send them to be analized
    # switch(classify_arguments(cmd), info)
    switch(cmd, info)


def switch(command: list[str], info: object) -> None:

    # Match the command name to the corresponding file in ./cmd/
    # for further processing and execution

    from . import cmd as fluxcmd

    exec_command: fluxcmd.helpers.commands.CommandInterface

    if command[0] in info.ignored_commands:
        if command[0] in info.user.background_tasks:
            print(f"Command {command[0]} is already in execution in background")
            return

    elif command[0] == "export":
        exec_command = fluxcmd.export.Command()
   
    elif command[0] == "flux":
        exec_command = fluxcmd.flux.Command()

    elif command[0] == "joke":
        exec_command = fluxcmd.joke.Command()
    
    elif command[0] == "observer":
        exec_command = fluxcmd.observer.Command()
    
    elif command[0] == "set":
        exec_command = fluxcmd.set.Commmand()
    
    try:
        exec_command.init()
        exec_command.run(command, info)
    except UnboundLocalError:
        if command[0] != "":
            print(f"-flux: {command[0]}: command not found\n")
