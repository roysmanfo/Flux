import os

from core import setup
from settings.info import User, Path

setup_result = setup.setup(user=User, path=Path)
USER: User = setup_result[0]
PATH: Path = setup_result[1]

print(PATH.documents)
print(USER.paths)
