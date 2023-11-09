from ...helpers.commands import *
from ...helpers.arguments import Parser
import shutil
import os

class Command(CommandInterface):
    def init(self):
        self.parser = Parser("cp", description="Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY")

        self.parser.add_argument('source', nargs='+', help='the file(s) or directory(s) to copy')
        self.parser.add_argument('dest', help='the destination of the sources')
        self.parser.add_argument('-f', '--force', action='store_true', help='if an existing destination file cannot be opened, remove it and try again (ignored if -n is also used)')
        self.parser.add_argument('-i', '--interactive', action='store_true', help='prompt before overwrite (overrides a previous -n)')
        self.parser.add_argument('-n', '--no-clobber', action='store_true', help='do not overwrite an existing file (overrides previus -i)')
        self.parser.add_argument('-R', '-r', '--recursive', action='store_true', help='copy directories recursively')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='explain what is being done')

    def run(self):

        for i in self.args.source:
            if not os.path.exists(i):
                self.error(self.logger.file_not_found(i))
                return

        # Handle multiple files given as source to copy
        if len(self.args.source) > 0 or not os.path.exists(self.args.dest) or not os.path.isdir(self.args.dest):            
            try:
                os.makedirs(self.args.dest)

            except PermissionError:
                self.error(self.logger.permission_denied(self.args.dest))
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
                
        dest = self.args.dest            
        for path in self.args.source:
            
            if os.path.isdir(path):
                self.copy_folder(path)
            
            elif os.path.isfile(path):
                self.copy_file(path)

            # reset the destination if it has been modified (es. in copy_file())
            self.args.dest = dest

            print()

        
    def copy_folder(self, path: str):
        if not self.args.recursive:
            self.warning(self.logger.parameter_not_specified('-r') + f"; omitting directory {path}")
            return
        
        try:
            before = os.listdir(path)
            after = os.listdir(shutil.copytree(path, self.args.dest, dirs_exist_ok=True))
            after = [os.path.join(self.args.dest, path) for path in after]
            
            if self.args.verbose:
                for path in before:
                    self.print(f"'{path}' -> '{after[before.index(path)]}'")

        except PermissionError:
            self.error(self.logger.permission_denied(path))
            return


    def copy_file(self, path: str):
        if os.path.exists(self.args.dest):
            if self.args.no_clobber:
                return
            
            if os.path.exists(self.args.dest) and os.path.isdir(self.args.dest):
                self.args.dest = os.path.join(self.args.dest, os.path.basename(path))

            if self.args.interactive and os.path.exists(self.args.dest) and os.path.isfile(self.args.dest) :
                overwrite = self.stdin.read().strip() if self.stdin.readable() else ''

                while not overwrite.lower().strip() in ['y', 'n']:
                    overwrite = input(f"cp: overwrite '{self.args.dest}'? ")
                    if not overwrite.lower().strip() in ['y', 'n']:
                        print("please specify 'y' or 'n'")

                if overwrite == 'n':
                    return
        
        if not os.path.exists(os.path.dirname(self.args.dest)) and os.path.dirname(self.args.dest) != '':
            try:
                os.makedirs(os.path.dirname(self.args.dest))

            except PermissionError:
                self.error(self.logger.permission_denied(path))
                return

        try:
            shutil.copy(path, self.args.dest)

            if self.args.verbose:
                self.print("'{}' -> '{}'".format(path, self.args.dest))
                
        except shutil.SameFileError:
            self.warning(self.logger.same_file(path, self.args.dest))

        except PermissionError:
            self.error(self.logger.permission_denied(self.args.dest))
