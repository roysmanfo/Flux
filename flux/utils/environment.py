import sys
from typing import Optional, Tuple
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

    return all([
            is_in_venv(),
            os.path.exists(os.path.join(venv_l, ".fluxenv")),
            
            # following condition may be added later, for now it will take any activated fluxenv
            # venv_l == os.path.expanduser(".flux/venv")
        ])


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

    return os.path.splitext(os.path.basename(sys.executable.replace('python', 'pip')))[0]
