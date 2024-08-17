import os
import importlib
from functools import lru_cache as _lru_cache
from typing import Callable, Optional, TextIO

# List of directories to search for custom scripts/extensions
custom_script_dirs = ["fpm"]
manager_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# store up to 50 commands in the cache
max_cache_size = 50


@_lru_cache(maxsize=max_cache_size, typed=False)
def load_custom_script(script_name: str) -> Optional[Callable[[object, str, str, bool, TextIO, TextIO, TextIO, int], None]]:
    """
    Load an external command installed on the machine
    """

    for dir_name in custom_script_dirs:
        script_path = os.path.join(dir_name, script_name + ".py")
        if os.path.isfile(script_path):
            try:
                module = importlib.import_module(f"{dir_name}.{script_name}")
                exec_command_class = getattr(module, "Command")
                return exec_command_class
            except (ImportError, AttributeError):
                pass
    return None

@_lru_cache(maxsize=max_cache_size, typed=False)
def load_builtin_script(script_name: str) -> Optional[Callable[[object, str, str, bool, TextIO, TextIO, TextIO, int], None]]:
    """
    Load an internal command installed on the machine
    """
    dir_name = os.path.join(manager_dir, "cmd", "builtin")
    script_path = os.path.join(dir_name, script_name + ".py")
    if os.path.exists(script_path) and os.path.isfile(script_path):
        try:
            module = importlib.import_module(f"flux.core.cmd.builtin.{script_name}", "flux")
            try:
                if hasattr(module, "ENTRY_POINT"):
                    class_name = getattr(module, "ENTRY_POINT")
                    if not hasattr(module, class_name):
                        class_name = ""
                else:
                    class_name = "Command"
            except AttributeError:
                class_name = "Command"
            finally:
                return getattr(module, class_name) if class_name else None

        except (ImportError, AttributeError):
            pass

    return None

@_lru_cache(maxsize=max_cache_size, typed=False)
def load_service(service_name: str) -> Optional[Callable[[object, str], None]]:
    """
    Load a service installed on the machine
    """
    dir_name = os.path.join(manager_dir, "services")
    script_path = os.path.join(dir_name, service_name + ".py")

    if os.path.exists(script_path) and os.path.isfile(script_path):
        try:
            module = importlib.import_module(f"flux.core.services.{service_name}", "flux")
            try:
                if hasattr(module, "ENTRY_POINT"):
                    class_name = getattr(module, "ENTRY_POINT")
                    if not hasattr(module, class_name):
                        class_name = ""
                else:
                    class_name = "Service"
            except AttributeError:
                class_name = "Service"
            finally:
                return getattr(module, class_name) if class_name else None

        except (ImportError, AttributeError):
            pass

    return None
