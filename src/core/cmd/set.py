"""
# `cr set`
Allows the user to change different settings, such as the username or USER.path informations
"""
from pathlib import Path


OPTIONS = []
FLAGS = ['--reset', '--all']


def run(command: dict, info: object):
    """
    Handles which setting to change 
    """
    switch(command, info)


def switch(command: dict, info: object):
    """
    Assigns the input to the right function 
    """
    USER = info.user

    if command["variables"]:

        # Change username
        if command["variables"][0] == "username":
            USER.set_username(command["variables"][1])

        # Set 1 or more new bg-task/s
        elif command["variables"][0] == "bg-task":
            command["variables"].pop(0)
            USER.set_bg_task(info, list(command["variables"]))

        # Set/ change an email
        # if muliple emails given, set as email the first valid one
        elif command["variables"][0] == "email":
            command["variables"].pop(0)
            USER.set_email(info, list(command["variables"]))

        # change a Path
        elif command["variables"][0].startswith("path.") and len(command["variables"][0].split(".")) == 2:
            target = command["variables"][0].split(".")[1]
            USER.paths.set_path(target, Path(command["variables"][1]))

    elif command["flags"]:

        # Reset all user vareables
        if "--reset" in command["flags"] and "--all" in command["flags"]:
            USER.reset_settings()
            print('Restart the shell to apply changes')

        else:
            print('Command not found')
