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

    classified["command"] = command[0]
    classified["flags"] = flags
    classified["variables"] = variables
    classified["options"] = options

    return classified


def manage(cmd: list):
    command = classify_arguments(cmd)