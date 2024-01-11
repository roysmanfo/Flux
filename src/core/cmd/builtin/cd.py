from ...helpers.arguments import Parser
from ...helpers.commands import *
import os


class Command(CommandInterface):
    def init(self):
        self.parser = Parser(
            prog="cd", description="Change the current directory to DIR.  The default DIR is the value of the HOME shell variable.")
        self.parser.add_argument("dir", nargs="*")

    def setup(self):
        super().setup()
        if len(self.args.dir) > 1:
            self.error(self.errors.too_many_args())
        else:
            self.args.dir = self.args.dir[0]

    def run(self):
        if self.args.dir:
            try:
                new_dir: str = "" + self.args.dir.strip('"').strip("'")
                if new_dir.startswith("$"):
                    new_dir = self.info.variables.get(new_dir).value or new_dir
                os.chdir(f"{new_dir}")
                self.info.variables.set("$PWD", new_dir)

            except FileNotFoundError:
                self.error(self.errors.path_not_found(new_dir))

            except NotADirectoryError:
                self.error(self.errors.not_a_dir(new_dir))

            except OSError:
                self.error(self.errors.cannot_read_fod(new_dir))

            self.info.user.paths.terminal = os.getcwd()
            self.info.user.paths.terminal.replace("\\", "/")

        else:
            os.chdir(self.info.variables.get("$HOME").value)
            self.info.user.paths.terminal = self.info.variables.get("$HOME").value
            self.info.variables.set("$PWD", self.info.user.paths.terminal)
