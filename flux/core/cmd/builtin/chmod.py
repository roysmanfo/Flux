from typing import Any
from flux.core.helpers.commands import *
from flux.core.helpers.arguments import Parser

import os


class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog="chmod", description="Change the mode of each FILE to MODE")
        self.parser.add_argument("MODE",  help="the new owner (can be [OWNER] or [OWNER]:[GROUP])")
        self.parser.add_argument("FILE", nargs="+", help="the file/s to modify")

    def run(self):
        
        for f in self.args.FILE:
            if not os.path.exists(f):
                self.error(self.errors.file_not_found(f))


        mode = self.args.mode

        for file in self.args.FILE:
            file: str

            try:
                os.chmod(file, mode)

            except Exception as e:
                self.error(e.__str__())


