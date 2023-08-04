"""
# `flux joke`

This command tells a random programming joke
"""

from .helpers import jokes
from .helpers.commands import CommandInterface
import random


class Command(CommandInterface):
    
    @staticmethod
    def run(command: list[str], info: object):
        """
        This command tells a random programming joke
        """
        print(random.choice(jokes.jokes))
        print()
