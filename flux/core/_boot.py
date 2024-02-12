import os
import platform
import subprocess
from typing import List, Optional
import logging

from flux.utils import environment

class _Warning:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description


class _Report:
    def __init__(self) -> None:
        self.can_start = True
        self.warnings: List[_Warning] = []


report = _Report()
root_dir = os.path.realpath(os.path.join(
    os.path.realpath(__file__), "..", "..", ".."))

def boot(dev_mode: bool = False) -> _Report:
    """
    Handles environment and minimum dependencies, and makes 
    `:param dev_mode`: if set to True, outputs on stdout all output
    `:returns` : A _Report object that determines if the application can start without problems
    """

    if dev_mode:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)

    logging.debug("checking virtual environment")
    if environment.is_in_venv():
        logging.debug(f"found virtual environment: {environment.get_venv_name()} ({environment.get_venv_location()})")
        # TODO: check requirements, and install them if necessary
        report.can_start = handle_min_requirements()
        return report

    return report


def install_requirements(dep: List[str]) -> Optional[subprocess.CompletedProcess]:
    try:
        interp = environment.get_interpreter_command()
        pip = environment.get_pip_command()
        command = [interp, "-m", pip, "install"]

        logging.info(f"installing: {'\n  -  '.join(dep)}")
        subprocess.run(command + ["--upgrade", "--user", pip],
                       capture_output=(logging.root.level > logging.DEBUG), text=True, check=True)
        return subprocess.run(command + dep, capture_output=(logging.root.level > logging.DEBUG), text=True, check=True)
    except subprocess.CalledProcessError as e:
        report.warnings.append(_Warning(e.__class__.__name__, e.stderr))


def get_minimum_requirements() -> Optional[List[str]]:
    """
    `:returns` : A list containing all minimum dependencies needed or None in case of error (es. FileNotFound, IOError, ...)   
    """
    req = os.path.join(root_dir, "requirements.txt")

    if os.path.exists(req):
        try:
            with open(req) as file:
                requirements = file.read().splitlines()

                OS_NAME = platform.system().lower()

                if OS_NAME.startswith("win"):
                    requirements += get_windows_requirements()
                elif OS_NAME in ["linux", "darwin"]:
                    requirements += get_linux_requirements()

                return requirements

        except:
            # error reading file
            return None
    # file does not exist
    return None


def get_windows_requirements() -> List[str]:
    """
    Requirements specific to windows
    """

    dep = [
        "mutagen==1.47.0",
        "pydub==0.25.1",
        "PyPDF2==3.0.1",
        "python-magic-bin==0.4.14",
    ]

    return dep


def get_linux_requirements() -> List[str]:
    """
    Requirements specific to linux
    """

    dep = [
        "mutagen==1.47.0",
        "pydub==0.25.1",
        "PyPDF2==3.0.1",
    ]

    return dep


def handle_min_requirements() -> bool:
    """
    `:returns` : True if all the minimum requirements are/have been installed, False otherwhise 
    """
    minim = get_minimum_requirements()

    if not minim:
        return False

    import importlib.util
    to_install = []
    wrong_version: list[tuple[str, str]] = []

    try:
        result = subprocess.run([environment.get_interpreter_command(), "-m", environment.get_pip_command(), "freeze"], text=True)
        packages = result.stdout.split('\n')
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        packages = None
        report.warnings.append(_Warning(e.__class__.__name__, e.__str__()))
    
    for req in minim:
        req_parts = req.split("==")
        if (not importlib.util.find_spec(req_parts[0])):
            to_install.append(req)
        else:
            # requirement installed, check version
            if packages:
                for package in packages:
                    # check the name and version
                    if package.startswith(req_parts[0]) and package.split('==')[-1] != req_parts[-1]:
                        # wrong version
                        wrong_version.append((req, package))
                        report.warnings.append(
                            _Warning(
                                "Wrong version",
                                f"Package {req_parts[0]} found with version {package.split("==")[-1]} instead of {req_parts[-1]}"
                                )
                            )
            else:
                report.warnings.append(_Warning("Unable to check package version", ""))
                
                

    if to_install:
        p = install_requirements(to_install)
        return p is not None and p.returncode == 0

    return True
