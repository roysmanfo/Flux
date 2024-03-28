import platform
import sys
from typing import List, Optional, Tuple
import os




def get_venv() -> Optional[Tuple[str, str]]:
    """
    `:returns` : a tuple containing the virtual environment location and type (VENV | CONDA)
    `:rtype`   : tuple[str, str] | None
    """
    if os.getenv("VIRTUAL_ENV"):
        return os.getenv("VIRTUAL_ENV"), "VIRTUAL_ENV"
    elif os.getenv("CONDA_PREFIX"):
        return os.getenv("CONDA_PREFIX"), "CONDA_PREFIX"
    return None

def get_venv_location() -> Optional[str]:
    """
    `:returns` : returns the virtual environment location
    `:rtype`   : str | None
    """
    venv = get_venv()
    return None if not venv else venv[0]

def get_venv_name() -> Optional[str]:
    venv = get_venv_location()
    return None if not venv else os.path.basename(venv)


def is_in_venv() -> bool:
    """
    `:returns` : True if the application is running in a virtual environment  
    `:rtype`   : bool
    """
    return get_venv() is not None


def is_in_flux_env() -> bool:
    """
    `:returns` : True if the application is running in a Flux virtual environment  
    `:rtype`   : bool
    """
    venv_l = get_venv_location()

    return is_flux_env(venv_l)

def is_venv(path: str) -> bool:
    """
    Check if the path provided points to a 'usable' virtual environment
    `:returns` : True if the path points to a virtual environment
    `:rtype`   : bool
    """

    if not os.path.isdir(path):
        return False
    conditions = False

    folder = os.path.abspath(path)
    if os.path.exists(os.path.join(folder, "pyvenv.cfg")):
        bins = ""
        extension = ""
        plat = platform.system().lower()

        if plat.startswith("win"):
            bins = "Scripts"
            extension = '.exe'
        elif plat in ['linux', 'darwin']:
            bins = "bin"
        
        conditions = all([
            os.path.exists(os.path.join(folder, bins, "activate")),
            os.path.exists(os.path.join(folder, bins, f"python{extension}")),
            os.path.exists(os.path.join(folder, bins, f"pip{extension}")),
        ])
    return conditions

def is_flux_env(path: str) -> bool:
    """
    `:returns` : True if the provided path points to a Flux virtual environment  
    `:rtype`   : bool
    """

    return all([
            is_venv(path),
            os.path.exists(os.path.join(path, ".fluxenv")),               
        ])

def list_venvs(path: str) -> List[str]:
    """
    Search every folder in `path` for a pyvenv.cfg file
    `:returns` : a list containing all vintualenv paths detected in a folder
    `:rtype`   : list[str]
    """
    venvs = []
    if os.path.isdir(path):
        for folder in os.listdir(path):
            if is_venv(os.path.join(path, folder)):
                venvs.append(folder)
    return venvs


def get_interpreter_path() -> str:
    """
    `:returns` : the path of th python interpreter in use
    `:rtype`   : str
    """

    return sys.executable


def get_interpreter_command() -> str:
    """
    `:returns` : the command to use in order to interact with the python interpreter cli
    `:rtype`   : str
    """

    return os.path.splitext(os.path.basename(get_interpreter_path()))[0]


def get_pip_command() -> str:
    """
    `:returns` : the command to use in order to interact with the python pip package manager
    `:rtype`   : str
    """

    # well this doesn't always work, so just stick to pip and forget about pip3
    # return os.path.splitext(os.path.basename(sys.executable.replace('python', 'pip')))[0]

    return "pip"
