"""
Necessary procedures to prepare the program to work
as intended.
"""
import os
from src.settings.info import User, Info

def setup() -> Info:
    """
    ## Setup process

    This process retrives all data necessary to start using Flux, like
    User setings, file locations on the disk, etc.

    This process makes it easier to start Flux as we just need to call this
    function in the main file and everything will be handled automaticaly. 

    Returns
    -------
    @returns : An object of type Info
    """

    # Load user
    USER = User()
    os.chdir(USER.paths.terminal)

    INFO = Info(USER)
    return INFO

