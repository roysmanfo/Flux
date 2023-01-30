"""
# `cr set`
Allows the user to change different settings, such as the username or USER.path informations
"""

OPTIONS = []
FLAGS = []

def run(command: dict, info: object):
    """
    Handles which setting to change 
    """
    switch(command, info)

def switch(command: dict, info: dict):
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

        else:
            with open(info.lang_file, 'r') as f:
                print(f.readlines()[2])
        
    
    
    