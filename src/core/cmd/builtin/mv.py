from ...helpers.commands import *
from ...helpers.arguments import Parser

import os 
import shutil

class Command(CommandInterface):
    
    def init(self):
        self.parser = Parser(prog='mv', add_help=True, description='Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.')

        self.parser.add_argument('source', nargs='+', help='the file(s) or directory(s) to copy')
        self.parser.add_argument('dest', help='the destination of the sources')
        self.parser.add_argument('-f', '--force', action='store_true', help='do not prompt before overwriting (overrides a previous -i or -n)')
        self.parser.add_argument('-i', '--interactive', action='store_true', help='prompt before overwrite (overrides a previous -n or -f)')
        self.parser.add_argument('-n', '--no-clobber', action='store_true', help='do not overwrite an existing file (overrides previus -i or -f)')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='explain what is being done')

    def run(self):
        """
        This command tells a random programming joke
        """

        for i in self.args.source:
            if not os.path.exists(i):
                self.error(STATUS_ERR, self.logger.file_not_found(i))
                return

        # Handle multiple files given as source to copy
        if len(self.args.source) > 0 or not os.path.exists(self.args.dest) or not os.path.isdir(self.args.dest):            
            try:
                os.makedirs(self.args.dest)

            except PermissionError:
                self.error(STATUS_ERR, self.logger.permission_denied(self.args.dest))
                return


        if self.args.interactive and self.args.no_clobber:
            a = ''
            i = ['-i', '--interactive']
            n = ['-n', '--no-clobber']

            for arg in self.command[::-1]:
                if arg in i + n:
                    a = arg
                    break

            if a in i:
                self.args.no_clobber = False
            else:
                self.args.interactive = False

        for path in self.args.source:
            if os.path.isdir(path):
                try:
                    self.args.source.extend(os.listdir(path))

                except PermissionError:
                    self.error(STATUS_ERR, self.logger.permission_denied(path))
                    return


        dest = self.args.dest            
        for path in self.args.source:            
            # self.move_file(path)
            pass
            # reset the destination if it has been modified (es. in copy_file())
            # self.args.dest = dest

        print()


                