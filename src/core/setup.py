"""
Necessary procedures to prepare the program to work
as intended.
"""
import os
import platform
from typing import List, Optional
from src.settings.info import User, Info, SysPaths
import subprocess


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
    
    OS_NAME = platform.system().lower()
    if OS_NAME.startswith("win"):
        install_windows_requirements()
    
    elif OS_NAME in ["linux", "darwin"]:
        install_linux_requirements()


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


def install_requirements(dep: List[str], verbose: Optional[bool] = None) -> Optional[subprocess.CompletedProcess]:
    try:
        arg = " ".join(dep)
        dep_list = '\n  -  '.join(dep)
        if not verbose:
            print(f"installing: {dep_list}")
        return subprocess.run([get_interpreter_command(), "install", arg], capture_output=(not verbose), text=True, check=True)
    except subprocess.CalledProcessError:
        return None


def install_windows_requirements() -> None:
    """
    Installs requirements specific to windows if not already found
    """

    dep = [
        "mutagen==1.47.0",
        "pydub==0.25.1",
        "PyPDF2==3.0.1",
        "python-magic-bin==0.4.14",
    ]

    p = install_requirements(dep, True)

    if p and p.returncode != 0:
        print(p.stderr)
    else:
        print("all requirements installed")
        


def install_linux_requirements() -> None:
    """
    Installs requirements specific to linux if not already found
    """

    dep = [
        "mutagen==1.47.0",
        "pydub==0.25.1",
        "PyPDF2==3.0.1",
    ]

    p = install_requirements(dep, True)
   
    if p and p.returncode != 0:
        print(p.stderr)
    else:
        print("all requirements installed")