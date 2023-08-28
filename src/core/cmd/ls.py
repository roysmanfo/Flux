from .helpers.commands import *
from .helpers.arguments import Parser
import os

from colorama import init as col_init, Fore, Back 

class Command(CommandInterface):

    def init(self):
        col_init(autoreset=True)
        self.parser = Parser(add_help=True, prog="ls", description="List information about the FILEs (the current directory by default).")
        self.parser.add_argument("PATH", nargs="?", default=self.info.user.paths.terminal, help="The path of the directory to list")
        self.parser.add_argument("-l", action="store_true", help="Use a long listing format")
        self.parser.add_argument("-a", dest="all", action="store_true", help="Do not ignore entries starting with .")

    def run(self, command: list[str]):
        self.args = self.parser.parse_args(command[1:])

        if self.parser.exit_execution:
            print()
            return

        if not os.path.exists(self.args.PATH):
            self.error(STATUS_ERR, f"cannot access '{self.args.PATH}': No such file or directory")
            return

        dir_contents = os.listdir(self.args.PATH)

        if not self.args.all:
            dir_contents = [i for i in dir_contents if not i.startswith(".")]

        output = ""
        for content in dir_contents:
            if os.path.isdir(content):
                output += f"{Fore.LIGHTBLUE_EX}{content}  "
            elif os.path.isfile(content):
                output += f"{Fore.CYAN}{content}  "

        self.stdout.write(output + "\n\n")

        

