"""
Necessary procedures to prepare the program to work
as intended.
"""
import os
from typing import Optional

from flux.settings.info import User, Info, SysPaths
from . import fboot



def setup(dev_mode: bool = False) -> Optional[Info]:
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

    if not _boot(dev_mode):
        return None
    return _system_setup()


def _boot(dev_mode: bool) -> bool:
    report = fboot.boot(dev_mode)
    
    if dev_mode and report.warnings or not report.can_start:
        for w in report.warnings:
            print(w)
    
    if not report.can_start:
        return False
    return True


def _system_setup() -> Info:
    # Load user
    SYS_PATHS = SysPaths()
    SYS_PATHS.create_initial_folders() # May rise an exception
    
    USER = User()
    os.chdir(USER.paths.terminal)

    INFO = Info(USER, SYS_PATHS)
    return INFO