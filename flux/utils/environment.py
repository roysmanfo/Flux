import sys
import subprocess
from typing import Optional


def is_in_venv() -> bool:
    return hasattr(sys, 'real_prefix')

def get_venv_name() -> str | None:
    return sys.prefix if is_in_venv() else None

def get_interpreter_command() -> Optional[str]:
    """
    `:returns` : the command to use in order to interact with the python interpreter cli, None if not found
    `:dtype`   : str or None
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

def get_pip_command() -> Optional[str]:
    """
    `:returns` : the command to use in order to interact with the python pip package manager, None if not found
    `:dtype`   : str or None
    """

    commands = [
        ("pip3", "--version"),
        ("pip", "--version"),        
    ]

    for c in commands:
        try:
            p = subprocess.run(c, capture_output=True)
            if p and p.stdout:
                return c[0]
        except:
            pass

    return None