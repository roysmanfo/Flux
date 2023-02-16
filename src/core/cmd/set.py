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
        
        # Try to set a variable
        set_a_variable = set_user_variable(command, info)
        
        if set_a_variable:
            return

        # Change username
        if command["variables"][0] == "username":
            USER.set_username(command["variables"][1], info)

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
            USER.paths.set_path(target, Path(command["variables"][1]), info)

    elif command["flags"]:

        # Reset all user vareables
        if "--reset" in command["flags"] and "--all" in command["flags"]:
            USER.reset_settings()
            print('Restart the shell to apply changes')

    else:
        
        print('Command not found')


def set_user_variable(command: dict, info: object) -> bool:
    """
    Allows the user to create temporary variables for later use.
    
    #### Create/update a variable
    ```
    $ cr set $var_name value
    ```

    #### Access a variable
    ```
    $ cr $var_name
    ```

    #### Returns

    True if the variable has been set, False otherwise
    """

    # Create a temporary variable if it doesn't already exist
    # else update it
    if len(command["variables"]) > 1 and command["variables"][0].startswith("$") and len(command["variables"][0]) > 1:
        key = command["variables"][0].removeprefix("$")
        value = str(command["variables"][1])
        
        info.variables[key] = value.removeprefix("\"").removesuffix("\"")
        print(f"${key} = {value}")
        return True
    
    
    return False