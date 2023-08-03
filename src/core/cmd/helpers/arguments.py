from argparse import HelpFormatter, ArgumentParser
import sys as _sys


class Parser(ArgumentParser):
    """
    `argparse.ArgumentParser` adaptation for program based parsing.

    Works kinda like argparse but excluding its default behaviours
    like exiting the program on the firs parsing error.
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
                 add_help=False,
                 allow_abbrev=True,
                 exit_on_error=True) -> None:
        super().__init__(prog, usage, description, epilog, parents, formatter_class, prefix_chars, fromfile_prefix_chars,
                         argument_default, conflict_handler, add_help, allow_abbrev, exit_on_error)
        
        self.parsing_error = False
        self.help_message = ""
        if not add_help:
            self.add_argument("-h", "--help", action="store_true", help="Show this help message")


    def exit(self, status: int | None = None, message: str | None = None):
        if message:
            self._print_message(message, _sys.stderr)
            print()
            self.parsing_error = True

    def add_help_message(self, message: str):
        self.help_message = message.strip()

    def help(self, message: str | None = None):
        print(message) if message else print(self.help_message)
        print()