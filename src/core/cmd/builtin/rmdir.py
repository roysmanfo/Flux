from ...helpers.commands import *
from ...helpers.arguments import Parser

import os
class Command(CommandInterface):
    def init(self):
        self.parser = Parser("rmdir", description="Remove the DIRECTORY(ies), if they are empty")
        self.parser.add_argument('path', nargs="+", help="the path of the directory to create")
        self.parser.add_argument('-m', '--mode', type=int, default=511, help="set file mode (as in chmod), not a=rwx - umask")
        self.parser.add_argument('-p', '--parents', action='store_true', help="no error if existing, make parent directories as needed, with their file modes unaffected by any -m option")
        self.parser.add_argument('-v', '--verbose', action='store_true', help="print a message for each created directory")


    def run(self):
        for folder in self.args.path:

            if not os.path.exists(folder):
                self.error(self.logger.path_not_found(folder))

            elif len(os.listdir(folder)) > 0 :
                self.error(f"rmdir: failed to remove `{folder}`: Directory not empty")
            
            else:
                try:
                    if not self.args.parents:
                        os.rmdir(folder)
                    else:
                        os.removedirs(folder)

                    if self.args.verbose:
                        self.print("rmdir: removing directory '{}'".format(folder))
                
                except PermissionError:
                    self.error(self.logger.permission_denied(folder))
                
                except OSError:
                    self.error(self.logger.path_not_found(folder))



        



