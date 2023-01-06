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
        
        if command["variables"][0] == "username":
            USER.set_username(command["variables"][1])
    
        else:
            with open(info.lang_file, 'r') as f:
                print(f.readlines()[2])
    
    
    