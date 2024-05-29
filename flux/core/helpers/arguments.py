from argparse import HelpFormatter, ArgumentParser
import sys as _sys
from typing import Optional


class Parser(ArgumentParser):
    """
    `argparse.ArgumentParser` adaptation for program based parsing.

    Works kinda like argparse but excluding its default behaviours
    like exiting the program on the first parsing error.
    """

    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 parents=[],
                 formatter_class=HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=True,
                 allow_abbrev=True,
                 exit_on_error=True) -> None:
        super().__init__(prog, usage, description, epilog, parents, formatter_class, prefix_chars, fromfile_prefix_chars,
                         argument_default, conflict_handler, add_help, allow_abbrev, exit_on_error)

        self.exit_execution = False
        self.help_message = ""
        self.ignored = []
        if not add_help:
            self.add_argument("-h", "--help", action="store_true")

    def error(self, message):
        if message and message not in self.ignored:
            self._print_message(message, _sys.stderr)
            self.exit_execution = True
            print()

    def exit(self, status: Optional[int] = None, message: Optional[str] = None):
        # Check if the help message has been shown
        if not message and not status:
            self.exit_execution = True
            return
        if message:
            self._print_message(message, _sys.stderr)
            self.exit_execution = True
            print()

    def add_help_message(self, message: str):
        self.help_message = message.strip()

    def help(self, message: Optional[str] = None):
        print(message) if message else print(self.help_message)
        print()
