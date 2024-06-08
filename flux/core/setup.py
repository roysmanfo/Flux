"""
Necessary procedures to prepare the program to work
as intended.
"""
import os
from typing import Optional
import subprocess

from flux.core.system.system import System
from flux.settings.settings import User, Settings, SysPaths



def setup() -> System:
    """
    ## Setup process

    This process retrives all data necessary to start using Flux, like
    User setings, file locations on the disk, etc.

    This process makes it easier to start Flux as we just need to call this
    function in the main file and everything will be handled automaticaly. 

    * `:returns` : An object containing system information
    * `:dtype`   : Settings
    * `:raises`  : PermissionError if the folders could not be created
    """
    
    # Load user
    SysPaths.create_initial_folders() # May rise an exception
    
    user = User()

    settings = Settings(user)
    system = System(settings)
    
    os.chdir(system.variables.get("$HOME").value)
    return system


def get_interpreter_command() -> Optional[str]:
    """
    `:returns` : the command to use in order to interact with the python interpreter cli, None if not found
    `:dtype`   : str | None
    """

    commands = [
        ("python3", "--version"),
        ("python", "--version"),
        
        # found on Windows
        ("py", "--version"),
    ]

    for c in commands:
        try:
            p = subprocess.run(c, capture_output=True)
            if p and p.stdout:
                return c[0]
        except:
            pass

    return None

