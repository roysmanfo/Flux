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

    :returns System: An object containing system information
    :raises PermissionError: if the folders could not be created
    """
    
    # Load user
    SysPaths.create_initial_folders() # May rise an exception
    
    user = User()

    settings = Settings(user)
    system = System(settings)
    
    os.chdir(system.variables.get("$HOME").value)
    return system

