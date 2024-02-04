"""
Necessary procedures to prepare the program to work
as intended.
"""
import os
import platform
from typing import List, Optional
import subprocess

from flux.settings.info import User, Info, SysPaths
from flux.utils import environment

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

    if not environment.is_in_venv():
        setup_exec_env()
        # print("creating venv")
        


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
        command = [get_interpreter_command(), "-m", "pip", "install"] + dep
        if not verbose:
            dep_list = '\n  -  '.join(dep)
            print(f"installing: {dep_list}")
        
        subprocess.run([get_interpreter_command(), "-m", "pip", "install", "--upgrade", "--user","pip"], capture_output=(not verbose), text=True, check=True)
        return subprocess.run(command, capture_output=(not verbose), text=True, check=True)
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

    if p and (p.returncode != 0 or p.stderr):
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
   
    if p and (p.returncode != 0 or p.stderr):
        print(p.stderr)
    else:
        print("all requirements installed")


def setup_exec_env() -> bool:
    """
    set up the system for execution
    """
    OS_NAME = platform.system().lower()

    venv_dir = os.path.join(os.path.abspath(".."), "venv")

    # a venv exists?
    if os.path.exists(venv_dir) and os.path.isdir(venv_dir):
        if os.path.exists(os.path.join(venv_dir, "pyvenv.cfg")):
            # move execution in the venv
            pass


    # if OS_NAME.startswith("win"):
    #     install_windows_requirements()
    
    # elif OS_NAME in ["linux", "darwin"]:
    #     install_linux_requirements()
