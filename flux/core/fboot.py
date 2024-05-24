"""
### Flux Boot (Flux's boot sequence)

These procedures allow flux to run in an isolated environment
and are necessary to handle missing requirements and ensure that Flux can start without issues
"""

import os
import subprocess
from typing import List, Optional
import logging

from flux.utils import environment

class _Warning:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def __str__(self) -> str:

        if not self.description:
            return f"[!] {self.name}"
        return f"[!] {self.name}: {self.description}"

class Report:
    def __init__(self) -> None:
        self.can_start = True
        self.already_run = False
        self.warnings: List[_Warning] = []


report = Report()
root_dir = os.path.realpath(os.path.join(
    os.path.realpath(__file__), "..", "..", ".."))

def boot(dev_mode: bool = False) -> Report:
    """
    Handles environment and minimum dependencies, and makes 
    `:param dev_mode`: if set to True, outputs on stdout all output
    `:returns` : A `Report` object that determines if the application can start without problems
    """

    if dev_mode:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    logging.debug("checking virtual environment")
    if environment.is_in_venv():
        logging.debug(f"found virtual environment: {environment.get_venv_name()} ({environment.get_venv_location()})")
        if not environment.is_in_flux_env():

            action = input(f"Environment {environment.get_venv_name()} does not contain a .fluxenv file, create one (y/n):  ").lower()
            if action == 'y':
                fluxenv = os.path.join(environment.get_venv_location(), ".fluxenv")
                logging.debug(f"creating file {fluxenv}")
                with open(fluxenv,'w') as f:
                    f.write("# This file was automaticaly created by Flux\n\n")

                logging.debug(f"fluxenv initialization completed")
            else:
                report.can_start = False
                report.warnings.append(_Warning("Not in flux environment", f"the .fluxenv file is missing in {environment.get_venv_location()}"))
                return report
        
        # check requirements, and install them if necessary
        logging.debug(f"checking requirements in {environment.get_venv_location()}")
        report.can_start = handle_min_requirements()
        logging.debug(f"fboot completed...    system setup")
        return report
    
    # check for an existing fluxenv (default name: venv) 
    logging.debug("no active environment")
    logging.debug("searching for default environment path")
    fenv = os.path.join(root_dir, "venv")
    logging.debug("looking for: %s" % fenv)

    if os.path.exists(os.path.join(root_dir, "venv")):
        if environment.is_flux_env(fenv):
            logging.debug(f"found flux environment: {fenv}")
            logging.debug(f"activating '{fenv}' and restarting the application")

            activate_environment(fenv)
            report.already_run = True
            return report
    
    
    # TODO: check all folders in the root_dir and look for venvs more specificaly fluxenvs 
    else:
        logging.debug(f"'{fenv}' not found")
        logging.debug(f"looking for all environments in {root_dir}")
        allvenvs = environment.list_venvs(root_dir)
        logging.debug(f"found {len(allvenvs)} venvs in '{root_dir}'")
        logging.debug(f"scanning results for flux environments...")
        for v in allvenvs:
            if environment.is_flux_env(v):
                fenv = v
                logging.debug(f"found flux environment: {fenv}")
                logging.debug(f"activating '{fenv}' and restarting the application")
                activate_environment(fenv)
                report.already_run = True
                return report
        
        # TODO: try to create new fluxenv
        logging.info("no flux environment found")
        resp = input("create a new flux environment? [y/n]: ").lower()

        if resp == 'y':
            import venv
            clear = False
            fenv = input("insert environment name (default: venv): ").lower().strip()
            fenv = fenv if fenv else "venv"
            
            while os.path.exists(fenv) and os.path.isdir(fenv):            
                resp = input(f"the directory {fenv} already exists, delete contents? [y/n]: ").lower()
                if resp == 'y':
                    clear=True
                    break

                fenv = input("insert environment name (default: venv): ").lower().strip()
                fenv = fenv if fenv else "venv"

            fenv = os.path.join(root_dir, fenv) # TODO: check if the path provided is a valid one first (fenv is a valid directory name)
            logging.info(f"creating flux environment in '{fenv}'")
            venv.create(fenv, clear=clear, prompt="fluxenv", with_pip=True)
            fluxenv = os.path.join(fenv, ".fluxenv")
            logging.debug(f"creating file {fluxenv}")
            with open(fluxenv,'w') as f:
                f.write("# This file was automaticaly created by Flux\n\n")
            logging.debug(f"activating '{fenv}'")
            logging.debug(f"restarting the application\n")
            activate_environment(fenv)
            report.already_run = True
            return report
        
    # if none of the options above worked, give up
    report.can_start = False
    report.warnings.append(_Warning("Unable to start", f"Flux is unable to complete the setup procedures"))
    return report


def install_requirements(dep: List[str]) -> Optional[subprocess.CompletedProcess]:
    try:
        interp = environment.get_interpreter_path()
        pip = environment.get_pip_command()
        command = [interp, "-m", pip, "install"]

        logging.info(f"upgrading pip")
        subprocess.run(command + ["--upgrade", pip], check=True)
        dps = '\n  -  '.join(dep)
        logging.info(f"installing: {dps}")
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

                if os.name == 'nt':
                    requirements += get_windows_requirements()
                else:
                    requirements += get_linux_requirements()

                # ensure no duplicates are present (NOTE: this isn't perfect, but works fine)
                return list(set(requirements)) 

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

    to_install = []
    wrong_version: list[tuple[str, str]] = []

    try:
        result = subprocess.run([environment.get_interpreter_path(), "-m", environment.get_pip_command(), "freeze"], capture_output=True, text=True)
        packages = result.stdout.split('\n')
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        packages = None
        report.warnings.append(_Warning(e.__class__.__name__, e.__str__()))
        return False

    package_names = []
    if packages:
        package_names = [i.split('==')[0].lower() for i in packages if i != '']
    else:
        report.warnings.append(_Warning("Unable to check package version", ""))

    for req in minim:
        req_parts = req.split("==")
        req_parts[0] = req_parts[0].lower()
        if (req_parts[0] not in package_names):
            to_install.append(req)
        else:
            # requirement installed, check version
            if packages:
                for package in packages:
                    # check the name and version
                    pkg_version = package.split('==')[-1]
                    if package.startswith(req_parts[0]) and pkg_version != req_parts[-1]:
                        # wrong version
                        wrong_version.append((req, package))
                        report.warnings.append(
                            _Warning(
                                "Wrong version found",
                                f"Package {req_parts[0]} found with version {pkg_version} instead of {req_parts[-1]}"
                                )
                            )

    if to_install:
        p = install_requirements(to_install)
        return p is not None and p.returncode == 0

    return True


def activate_environment(fenv: str) -> None:
    """
    Activates and runs the application from inside a virtual environment

    `:param fenv` the path to the flux virtual environment
    """

    shell_command = []
    python_script = os.path.join(root_dir, "flux", "main.py")

    if os.name == "nt":
        activate_script = os.path.join(fenv, "Scripts", "Activate.ps1")
        shell_command = [
            "powershell.exe",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            f"& '{activate_script}' ; python '{python_script}'{' --dev-mode' if logging.root.level <= logging.DEBUG else ''}"
        ]
    else:
        activate_script = os.path.join(fenv, "bin", "activate")
        shell_command = [
            "bash",
            "-c",
            f"source '{activate_script}' && python '{python_script}'{' --dev-mode' if logging.root.level <= logging.DEBUG else ''}"
        ]

    subprocess.run(shell_command)
