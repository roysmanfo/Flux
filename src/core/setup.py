"""
Necessary procedures to prepare the program to work
as intended.
"""
from . import bgtasks
import asyncio
from asyncio import AbstractEventLoop

def setup(user: object) -> tuple[object, str, str]:
    """
    ## Setup process

    This process retrives all data necessary to start using Cristal, like
    User setings, file locations on the disk, etc.

    This process makes it easier to start Cristal as we just need to call this
    function in the main file and everything will be handled automaticaly. 

    @param user : The user class from the info file in settings
    """
    from os import chdir

    # Load user
    USER = user()
    chdir(USER.paths.terminal)
    SYSTEM_CMDS, LANG_FILE = get_setup_settings(USER)




    return (USER, SYSTEM_CMDS, LANG_FILE)

def get_bgtasks(user: object) -> tuple[list[AbstractEventLoop], list[str]]:
    """
    Returns a list of all tasks the user decided to execute on starup and 
    a list of commands to ignore when called
    """
    from . import cmd as cr

    tasks = []
    ignore = []

    loop = asyncio.new_event_loop()

    bg = user.background_tasks
    # For each command check if the user decided to execute it on start
    if 'observer' in bg:

        ignore.append('observer')
        loop.create_task(cr.observer)

def get_setup_settings(user: object) -> list[str, str]:
    import platform, os
    from dotenv import load_dotenv

    load_dotenv(verbose=False)
    os.system("cls")


    if platform.system() == "Windows":
        # These commands will be executed from the default OS terminal (cmd.exe)
        SYSTEM_CMDS = os.getenv('WINDOWS')
        LANG_FILE: str = os.path.join(os.path.dirname(
            __file__)+"\\lang\\", user.language + ".txt")

    elif platform.system() in ["Linux", "Mac"]:
        # These commands will be executed from the default OS terminal (linux terminal)
        SYSTEM_CMDS = os.getenv('LINUX')
        LANG_FILE: str = os.path.join(os.path.realpath(
            __file__)+"/lang/", user.language + ".txt")

    return [SYSTEM_CMDS, LANG_FILE]