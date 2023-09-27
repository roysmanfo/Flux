"""
# `joke`

This command tells a random programming joke
"""

from ...helpers import jokes
from ...helpers.commands import CommandInterface
import random


class Command(CommandInterface):
    
    
    def run(self):
        """
        This command tells a random programming joke
        """
        self.stdout.write(random.choice(jokes.jokes))
        self.stdout.write("\n\n")
