"""
Necessary procedures to prepare the program to work
as intended.
"""
import os
import platform
from typing import Optional
import subprocess

from flux.settings.info import User, Info, SysPaths
from flux.utils import environment
from . import _boot



def setup() -> Info:
    """
    ## Setup process

    This process retrives all data necessary to start using Flux, like
    User setings, file locations on the disk, etc.

    This process makes it easier to start Flux as we just need to call this
    function in the main file and everything will be handled automaticaly. 

    * `:returns` : An object containing system information
    * `:dtype`   : Info
    * `:raises`  : PermissionError if the folders could not be created
    """

    if not environment.is_in_venv():
        import sys
        print("creating venv", environment.get_venv_name(), sys.prefix)
        # print(_boot.get_minimum_requirements())


    # if OS_NAME.startswith("win"):
    #     install_windows_requirements()
    
    # elif OS_NAME in ["linux", "darwin"]:
    #     install_linux_requirements()


    # Load user
    SYS_PATHS = SysPaths()
    SYS_PATHS.create_initial_folders() # May rise an exception
    
    USER = User()
    os.chdir(USER.paths.terminal)

    INFO = Info(USER, SYS_PATHS)
    return INFO


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

