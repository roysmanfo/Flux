from setuptools import setup, find_packages
from pathlib import Path
import os

DIR = Path(__file__).parent
VERSION_FILE = DIR / "flux" / "settings" / "version"
REQUIREMENTS_FILE = DIR / "requirements.txt"

with open(REQUIREMENTS_FILE, 'r') as fp: 
    REQUIREMENTS = fp.read().splitlines()

with open(VERSION_FILE, 'r') as fp:
    version = fp.read().splitlines()[0]
    VERSION = version if version else None

    if VERSION is None:
        raise RuntimeError("unable to determine flux version")

setup(
    name='flux',
    version=VERSION,
    author='roysmanfo',
    url='https://github.com/roysmanfo/flux',
    install_requires=REQUIREMENTS,
    packages=find_packages(where=".", exclude=("tests")),  # Use "." to find packages in the current directory
    package_dir={"": "."},  # Use "." to specify the root directory for packages
    package_data={
        "flux.security": ["public.pem"],
        "flux.settings": ["version"]
    },
    include_package_data=True,
    entry_points={
        'console_scripts': ['flux=flux.main:main']
    }
)
