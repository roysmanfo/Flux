"""
# `cr set`
Allows the user to change different settings, such as the username or USER.path informations
"""

OPTIONS = []
FLAGS = []

def run(command: dict, info: list):
    """
    Handles which setting to change 
    """
    switch(command, info)

def switch(command: dict, info: list):
    """
    Assigns the input to the right function 
    """
    USER = info[0]
    
    if command["variables"][0] == "username":
        USER.set_username(command["variables"][1].capitalize())
    
    else:
        with open(info[1], 'r') as f:
            print(f.readlines()[2])
    
    