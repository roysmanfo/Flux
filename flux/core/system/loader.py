import os
import importlib
from functools import lru_cache as _lru_cache
from types import ModuleType
from typing import Callable, Optional, TextIO

# List of directories to search for custom scripts/extensions
custom_script_dirs = ["scripts", "fpm"]
manager_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# store up to 50 commands in the cache
max_cache_size = 50


@_lru_cache(maxsize=max_cache_size, typed=False)
def load_custom_script(script_name: str) -> Optional[Callable[[object, str, str, bool, TextIO, TextIO, TextIO, int], None]]:
    """
    Load an external command installed on the machine
    """

    for dir_name in custom_script_dirs:
        script_path = os.path.join(manager_dir, "cmd", dir_name, script_name)
        if os.path.exists(script_path):
            if os.path.isfile(script_path + ".py"):
                try:
                    module = importlib.import_module(f"flux.core.cmd.{dir_name}.{script_name}.py")
                    importlib.import_module()
                    class_name = _get_entry_point(module)
                    return getattr(module, class_name) if class_name else None
                except ImportError:
                    pass
            elif os.path.isdir(script_path):
                try:
                    # in the case of 
                    module = importlib.import_module(f"flux.core.cmd.{dir_name}.{script_name}.main.py")
                    class_name = _get_entry_point(module)
                    return getattr(module, class_name) if class_name else None
                except ImportError:
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
            class_name = _get_entry_point(module)
            return getattr(module, class_name) if class_name else None

        except ImportError:
            pass

    return None

@_lru_cache(maxsize=max_cache_size, typed=False)
def _get_entry_point(module: ModuleType) -> Optional[str]:
    """
    resolve the entry point for this command
    
    (usually it is the class Command, unles ENTRY_POINT is set)
    """
    class_name = "Command"
    if hasattr(module, "ENTRY_POINT"):
        class_name = getattr(module, "ENTRY_POINT")
        if not class_name or not hasattr(module, class_name):
            # either ENRY_POINT=""  or the specified class does not exist
            class_name = None

    return class_name
  
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

