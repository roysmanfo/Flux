"""
# `flux joke`

This command tells a random programming joke
"""

from .helpers import jokes
import random


def run(command: dict, info: object):
    """
    This command tells a random programming joke
    """
    print(random.choice(jokes.jokes))
    print()
