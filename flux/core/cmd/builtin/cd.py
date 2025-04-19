from flux.core.helpers.commands import (
    CommandInterface,
    Parser,
    Status
)
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
        elif len(self.args.dir) == 1:
            self.args.dir = self.args.dir[0]
        else:
            self.args.dir = self.system.variables.get("$HOME").value

    def run(self):
        if self.args.dir:
            new_dir: str = "" + self.args.dir.strip('"').strip("'")
            if new_dir.startswith("$"):
                new_dir = self.system.variables.get(new_dir).value or new_dir

            if not os.path.exists(new_dir):
                self.error(self.errors.path_not_found(new_dir))

            elif not os.path.isdir(new_dir):
                self.error(self.errors.not_a_dir(new_dir))

            elif not os.access(new_dir, os.R_OK):
                self.error(self.errors.permission_denied(new_dir))

            else:                           
                self.settings.user.paths.terminal = os.path.realpath(new_dir).replace("\\", "/")

        else:
            self.settings.user.paths.terminal = self.system.variables.get("$HOME").value
        
        if self.status != Status.STATUS_ERR:
            self.system.variables.set("$PWD", self.settings.user.paths.terminal)
