"""
Necessary procedures to prepare the program to work
as intended.
"""
from . import bgtasks
import asyncio
from pathlib import Path


def setup(user: object, SETTINGS_FILE: Path, SETTINGS_FOLDER: Path) -> tuple[object, list[str], Path, list]:
    """
    ## Setup process

    This process retrives all data necessary to start using Cristal, like
    User setings, file locations on the disk, etc.

    This process makes it easier to start Cristal as we just need to call this
    function in the main file and everything will be handled automaticaly. 

    @param user : The user class from the info file in settings

    @returns : tuple[object, list, Path, list[AbstractEventLoop, list[str]]]

    - object:                                   The user instance from the info file in settings
    - list[str]:                                SYSTEM_CMDS, list off all commands of the os built-in terminal
    - Path:                                     LANG_FILE, Path to the file containing all the sentences in the prefered language
    - list[AbstractEventLoop], list[str]]:      All tasks to be executed on start, plus all commands to be ignored because of this
    """
    from os import chdir

    # Load user
    USER = user()
    chdir(USER.paths.terminal)
    SYSTEM_CMDS, LANG_FILE = get_setup_settings(USER)

    cmds = get_bgtasks([USER, LANG_FILE, SETTINGS_FILE, SETTINGS_FOLDER])

    return (USER, SYSTEM_CMDS, LANG_FILE, cmds)


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
        loop.create_task(cr.observer.run(info), name="Observer")

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
