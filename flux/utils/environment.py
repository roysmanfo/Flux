import sys


def is_in_venv() -> bool:
    return hasattr(sys, 'real_prefix')

def get_venv_name() -> str | None:
    return sys.prefix if is_in_venv() else None



