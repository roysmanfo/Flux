"""
Necessary procedures to prepare the program to work
as intended.
"""
from . import bgtasks
import asyncio
from pathlib import Path
from os import chdir


def setup(user: object, info: object, SETTINGS_FILE: Path, SETTINGS_FOLDER: Path) -> tuple[object, list[str], Path, list]:
    """
    ## Setup process

    This process retrives all data necessary to start using Cristal, like
    User setings, file locations on the disk, etc.

    This process makes it easier to start Cristal as we just need to call this
    function in the main file and everything will be handled automaticaly. 

    Parameters
    ----------
    @param user : The user class from the info file in settings/
    @param info : The info class from the info file in settings/
    @param SETTINGS_FILE : The SETTINGS_FILE costant from the info file in settings
    @param SETTINGS_FOLDER : The SETTINGS_FOLDER costant from the info file in settings

    Returns
    -------
    @returns : an object of type User
    @returns : an object of type Info
    """

    # Load user
    USER = user()
    chdir(USER.paths.terminal)
    SYSTEM_CMDS, LANG_FILE = get_setup_settings(USER)

    cmds = get_bgtasks([USER, LANG_FILE, SETTINGS_FILE, SETTINGS_FOLDER])

    INFO = info(USER, SYSTEM_CMDS, LANG_FILE,
                SETTINGS_FILE, SETTINGS_FOLDER, "", cmds)

    return (USER, INFO)


def get_bgtasks(info: list) -> list:
    """
    Returns a list of all tasks the user decided to execute on starup and 
    a list of commands to ignore when called
    """

    user = info[0]

    from . import cmd as cr

    tasks = []
    ignore = []

    loop = asyncio.new_event_loop()

    bg = user.background_tasks

    # For each command check if the user decided to execute it on start
    if 'observer' in bg:
        ignore.append('observer')
        command = {"command": "observer", "flags": [],
                   "variables": [], "options": []}
        loop.create_task(cr.observer.run(
            command=command, info=info, from_command_line=False), name="Observer")

    return [tasks, ignore]


def get_setup_settings(user: object) -> list:
    import platform
    import os
    from dotenv import load_dotenv

    load_dotenv(verbose=False)
    os.system("cls")

    if platform.system() == "Windows":
        # These commands will be executed from the default OS terminal (cmd.exe)
        SYSTEM_CMDS = os.getenv('WINDOWS').split(", ")
        LANG_FILE: Path = Path(os.path.join(os.path.dirname(
            __file__).replace("\\core", "")+"\\lang\\", user.language + ".txt"))

    elif platform.system() in ["Linux", "Mac"]:
        # These commands will be executed from the default OS terminal (linux terminal)
        SYSTEM_CMDS = os.getenv('LINUX').split(", ")
        LANG_FILE: Path = Path(os.path.join(os.path.realpath(
            __file__)+"/lang/", user.language + ".txt"))

    return [SYSTEM_CMDS, LANG_FILE]
