import os
import importlib

# List of directories to search for custom scripts/extensions
custom_script_dirs = ["scripts", "extensions"]
manager_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def load_custom_script(script_name: str):
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

def load_builtin_script(script_name: str):
    """
    Load an internal command installed on the machine
    """
    dir_name = os.path.join(manager_dir, "cmd", "builtin")
    script_path = os.path.join(dir_name, script_name + ".py")
    if os.path.exists(script_path) and os.path.isfile(script_path):
        try:
            cwd = os.getcwd()
            os.chdir(os.path.dirname(os.path.realpath(__file__)))
            module = importlib.import_module(f"src.core.cmd.builtin.{script_name}", "src")
            os.chdir(cwd)
            try:
                # TODO: Allow to specify a different name than 'Command' as class name
                # class_name = getattr(module, "ENTRY_POINT")
                class_name = "Command"
            except AttributeError:
                class_name = "Command"
            finally:
                exec_command_class = getattr(module, class_name)

            return exec_command_class
        except (ImportError, AttributeError) as e:
            pass
    return None