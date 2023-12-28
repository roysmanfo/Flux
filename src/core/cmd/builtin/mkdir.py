from ...helpers.commands import *
from ...helpers.arguments import Parser

import os
class Command(CommandInterface):
    def init(self):
        self.parser = Parser("mkdir", description="Create the DIRECTORY(ies), if they do not already exist")
        self.parser.add_argument('path', nargs="+", help="the path of the directory to create")
        self.parser.add_argument('-m', '--mode', type=int, default=511, help="set file mode (as in chmod), not a=rwx - umask")
        self.parser.add_argument('-p', '--parents', action='store_true', help="no error if existing, make parent directories as needed, with their file modes unaffected by any -m option")
        self.parser.add_argument('-v', '--verbose', action='store_true', help="print a message for each created directory")


    def run(self):
        for folder in self.args.path:

            if os.path.exists(folder):
                self.error(self.logger.file_exists(folder))
            
            else:
                try:
                    if not self.args.parents:
                        os.mkdir(folder, self.args.mode)
                    else:
                        os.makedirs(folder, self.args.mode, exist_ok=True)

                    if self.args.verbose:
                        self.print("mkdir: created directory '{}'".format(folder))
                
                except PermissionError:
                    self.error(self.logger.permission_denied(folder))
                
                except OSError:
                    self.error(self.logger.path_not_found(folder))



        



