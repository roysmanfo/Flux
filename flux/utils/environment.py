import subprocess
import sys
from typing import Optional, Tuple
import os


def get_venv() -> Optional[Tuple[str, str]]:
    """
    `:returns` : a tuple containing the virtual environment name and type (VENV | CONDA)
    `:rtype`   : tuple[str, str] | None
    """
    if os.getenv("VIRTUAL_ENV"):
        return os.path.basename(os.getenv("VIRTUAL_ENV")), "VENV"
    elif os.getenv("CONDA_PREFIX"):
        return os.path.basename(os.getenv("CONDA_PREFIX")), "CONDA"
    return None

def get_venv_name() -> Optional[Tuple[str, str]]:
    venv = get_venv()
    return None if not venv else venv[0]

def is_in_venv() -> bool:
    return get_venv() is not None

def get_interpreter_command() -> str:
    """
    `:returns` : the command to use in order to interact with the python interpreter cli, None if not found
    `:rtype`   : str
    """

    return os.path.splitext(os.path.basename(sys.executable))[0]

def get_pip_command() -> str:
    """
    `:returns` : the command to use in order to interact with the python pip package manager, None if not found
    `:rtype`   : str
    """

    return os.path.splitext(os.path.basename(sys.executable.replace('python', 'pip')))[0]