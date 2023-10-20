from ...helpers.commands import *
from ...helpers.arguments import Parser

import os 
import shutil

class Command(CommandInterface):
    
    def init(self):
        self.parser = Parser(prog='mv', add_help=True, description='Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.')

        self.parser.add_argument('source', nargs='+', help='the file(s) or directory(s) to copy')
        self.parser.add_argument('dest', help='the destination of the sources')
        self.parser.add_argument('-f', '--force', action='store_true', default=True, help='do not prompt before overwriting (overrides a previous -i or -n)')
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


        if self.args.force and self.args.interactive and self.args.no_clobber:
            a = ''
            i = ['-i', '--interactive']
            n = ['-n', '--no-clobber']
            f = ['-f', '--force']

            for arg in self.command[::-1]:
                if arg in i + n + f:
                    a = arg
                    break

            if a in i:
                self.args.no_clobber = False
                self.args.force = False
            elif a in n:
                self.args.interactive = False
                self.args.force = False
            else:
                self.args.no_clobber = False
                self.args.interactive = False


        for path in self.args.source:
            if os.path.isdir(path):
                try:
                    self.args.source.extend(os.listdir(path))
                    self.args.source.remove(path)

                except PermissionError:
                    self.error(STATUS_ERR, self.logger.permission_denied(path))
                    return

        self.args.source.sort()

        # dest = self.args.dest            
        for path in self.args.source:            
            self.move(path)


            # reset the destination if it has been modified (es. in copy_file())
            # self.args.dest = dest

        print()



    def move(self, path: str):
        d = self.args.dest if os.path.isdir(self.args.dest) else os.path.dirname(self.args.dest)
        final_path = os.path.join(self.args.dest, path)

        if os.path.exists(final_path):
            if self.args.no_clobber:
                return

            if self.args.interactive:
                overwrite = self.stdin.read().strip() if self.stdin.readable() else ''

                while not overwrite.lower().strip() in ['y', 'n']:
                    overwrite = input(f"cp: overwrite '{self.args.dest}'? ")
                    if not overwrite.lower().strip() in ['y', 'n']:
                        print("please specify 'y' or 'n'")

                if overwrite == 'n':
                    return
                

            if self.args.force:
                try:
                    os.remove(d)
                except PermissionError:
                    self.error(STATUS_ERR, self.logger.permission_denied(d))
                    return

        dest = shutil.move(path, d)

        if self.args.verbose:
            print('%s -> %s' % (path, dest))



