import os
import importlib
from functools import lru_cache as _lru_cache, _CacheInfo
from types import ModuleType
from typing import Callable, Optional, TextIO, Union
from pathlib import Path, WindowsPath, PosixPath

# List of directories to search for custom scripts/extensions
custom_script_dirs = ["scripts", "fpm"]
manager_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# store up to 50 commands in the cache
__initial_max_cache_size__ = 50
_max_cache_size = __initial_max_cache_size__
_search_priority: list[Path] = []

CommandInterfaceType = Callable[[object, list[str], bool, Optional[TextIO], Optional[TextIO], Optional[TextIO], int], None]


def use_cache(use: bool) -> None:
    global _max_cache_size
    _max_cache_size = 0 if not use else __initial_max_cache_size__

def set_search_priority(priority: list[Path]) -> None:
    """
    Set the search priority for the command loader
    """
    global _search_priority
    _search_priority = priority
    _search_priority = list(map(lambda p: Path(p) if not isinstance(p, (Path, WindowsPath, PosixPath)) else p, _search_priority))

def get_search_priority() -> list[Path]:
    """
    Get the search priority for the command loader
    """
    return _search_priority

def _load_module(module_name: str) -> ModuleType:
    module = importlib.import_module(f"flux.core.cmd.{module_name}", "flux")
    return importlib.reload(module)

@_lru_cache(maxsize=_max_cache_size, typed=False)
def load_command(script_name: str) -> Optional[CommandInterfaceType]:
    """
    Load a command installed on the machine
     
    If the `search_priority` has been set, it will search in the directories in the order specified
    """
    if not _search_priority:
        set_search_priority([
            Path(manager_dir, "cmd", "builtin"),
            Path(manager_dir, "cmd", "scripts"),
            Path(manager_dir, "cmd", "fpm"),
        ])


    for dir_path in _search_priority:
        script_path = os.path.join(dir_path, script_name)
        if os.path.exists(script_path + ".py") or os.path.isdir(script_path):
            if os.path.isfile(script_path + ".py"):
                try:
                    module = _load_module(f"{dir_path.name}.{script_name}")
                    class_name = _get_entry_point(module)
                    return getattr(module, class_name) if class_name else None
                except ImportError:
                    pass
            elif os.path.isdir(script_path):
                try:
                    module = _load_module(f"{dir_path.name}.{script_name}.main")
                    class_name = _get_entry_point(module)
                    return getattr(module, class_name) if class_name else None
                except ImportError:
                    pass
    return None

@_lru_cache(maxsize=_max_cache_size, typed=False)
def load_custom_script(script_name: str) -> Optional[CommandInterfaceType]:
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

@_lru_cache(maxsize=_max_cache_size, typed=False)
def load_builtin_script(script_name: str) -> Optional[CommandInterfaceType]:
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

@_lru_cache(maxsize=_max_cache_size, typed=False)
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


@_lru_cache(maxsize=_max_cache_size, typed=False)
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

def clear_loader_cache() -> None:
    """
    Clear the cache for the command loader
    """    
    load_command.cache_clear()
    load_custom_script.cache_clear()
    load_builtin_script.cache_clear()
    load_service.cache_clear()

def get_cache_info() -> dict[str, _CacheInfo]:
    """
    Get the cache info for the command loader
    """
    return {
        "load_command": load_command.cache_info(),
        "load_custom_script": load_custom_script.cache_info(),
        "load_builtin_script": load_builtin_script.cache_info(),
        "load_service": load_service.cache_info()
    }

def get_cache_parameters() -> dict[str, dict[str, Union[int, bool]]]:
    """
    Get the cache parameters for the command loader
    """
    return {
        "load_command": load_command.cache_parameters(),
        "load_custom_script": load_custom_script.cache_parameters(),
        "load_builtin_script": load_builtin_script.cache_parameters(),
        "load_service": load_service.cache_parameters()
    }


def get_cache_size() -> int:
    """
    Get the cache size for the command loader
    """

    return sum([i.currsize for i in get_cache_info().values() if i is not None])

def set_max_cache_size(size: int) -> None:
    """
    Set the max cache size for the command loader,
    if size is 0 or less, the cache will be reset to it's default value
    """
    global _max_cache_size
    _max_cache_size = size if size > 0 else __initial_max_cache_size__
    load_command.cache_clear()

