"""
Necessary procedures to prepare the program to work
as intended.
"""
from . import bgtasks
from threading import Thread
from pathlib import Path
from os import chdir


def setup(user: object, info: object, SETTINGS_FILE: Path, SETTINGS_FOLDER: Path) -> object:
    """
    ## Setup process

    This process retrives all data necessary to start using Flux, like
    User setings, file locations on the disk, etc.

    This process makes it easier to start Flux as we just need to call this
    function in the main file and everything will be handled automaticaly. 

    Parameters
    ----------
    @param user : The user class from the info file in settings/
    @param info : The info class from the info file in settings/
    @param SETTINGS_FILE : The SETTINGS_FILE costant from the info file in settings
    @param SETTINGS_FOLDER : The SETTINGS_FOLDER costant from the info file in settings

    Returns
    -------
    @returns : an object of type Info
    """

    # Load user
    USER = user()
    chdir(USER.paths.terminal)

    INFO = info(USER)
    return INFO



def get_setup_settings() -> list[str]:
    import platform
    import os
    from dotenv import load_dotenv

    load_dotenv(verbose=False)

    if platform.system() == "Windows":
        # These commands will be executed from the default OS terminal (cmd.exe)
        SYSTEM_CMDS = os.getenv('WINDOWS').split(", ")

    elif platform.system() in ["Linux", "Mac"]:
        # These commands will be executed from the default OS terminal (linux terminal)
        SYSTEM_CMDS = os.getenv('LINUX').split(", ")

    return SYSTEM_CMDS
