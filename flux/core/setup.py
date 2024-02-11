"""
Necessary procedures to prepare the program to work
as intended.
"""
import os

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
    * `:rtype`   : Info
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


