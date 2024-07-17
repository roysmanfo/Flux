from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)

import os
import shutil


class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog="chown", description="Change the owner and/or group of each FILE to OWNER and/or GROUP")
        self.parser.add_argument("owner",  help="the new owner (can be [OWNER] or [OWNER]:[GROUP])")
        self.parser.add_argument("file", nargs="+", help="the file/s to modify")

    def run(self):
        
        for f in self.args.file:
            if not os.path.exists(f):
                self.error(self.errors.file_not_found(f))


        for file in self.args.file:
            file: str
            owner: List[str] = [i for i in self.args.owner.split(":") if i]
            group = None
            
            if len(owner) > 2:
                self.error("illegal owner:group format")
                return

            if len(owner) == 2:
                group = owner[1]

            owner: str = owner[0]

            try:
                shutil.chown(file, owner, group)
            except Exception as e:
                self.error(e.__str__())


