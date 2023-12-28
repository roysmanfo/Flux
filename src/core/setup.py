"""
Necessary procedures to prepare the program to work
as intended.
"""
import os
from src.settings.info import User, Info, SysPaths

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

    # Load user
    SYS_PATHS = SysPaths()
    SYS_PATHS.create_initial_folders() # May rise an exception
    
    USER = User()
    os.chdir(USER.paths.terminal)

    INFO = Info(USER, SYS_PATHS)
    return INFO

