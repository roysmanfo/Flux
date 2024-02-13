"""
Necessary procedures to prepare the program to work
as intended.
"""
import os
from typing import Optional

from flux.settings.info import User, Info, SysPaths
from . import _boot



def setup() -> Optional[Info]:
    """
    ## Setup process

    This process retrives all data necessary to start using Flux, like
    User setings, file locations on the disk, etc.

    This process makes it easier to start Flux as we just need to call this
    function in the main file and everything will be handled automaticaly. 

    * `:returns` : An object containing system information, None in case of error
    * `:rtype`   : Info | None
    * `:raises`  : PermissionError if the folders could not be created
    """
    # TODO: add parameter to controll dev_mode
    report = _boot.boot()
    if not report.can_start:
        return None

    # Load user
    SYS_PATHS = SysPaths()
    SYS_PATHS.create_initial_folders() # May rise an exception
    
    USER = User()
    os.chdir(USER.paths.terminal)

    INFO = Info(USER, SYS_PATHS)
    return INFO


