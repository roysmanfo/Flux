from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)

from pathlib import Path
import os 
import shutil

class Command(CommandInterface):
    
    def init(self):
        self.parser = Parser(prog='mv', description='Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.')

        self.parser.add_argument('source', nargs='+', help='the file(s) or directory(s) to copy')
        self.parser.add_argument('dest', help='the destination of the sources')
        self.parser.add_argument('-f', '--force', action='store_true', default=True, help='do not prompt before overwriting (overrides a previous -i or -n)')
        self.parser.add_argument('-i', '--interactive', action='store_true', help='prompt before overwrite (overrides a previous -n or -f)')
        self.parser.add_argument('-n', '--no-clobber', action='store_true', help='do not overwrite an existing file (overrides previus -i or -f)')
        self.parser.add_argument('-T', '--no-target-directory', action='store_true', help='treat DEST as a normal file')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='explain what is being done')

    def run(self):
        """
        This command tells a random programming joke
        """

        for i in self.args.source:
            if not os.path.exists(i):
                self.error(self.errors.file_not_found(i))
                return

        # Handle multiple files given as source to copy
        if len(self.args.source) > 0 and (not os.path.exists(self.args.dest) or not os.path.isdir(self.args.dest)):
            if not self.args.no_target_directory:       
                try:
                    os.makedirs(self.args.dest) 

                except PermissionError:
                    self.error(self.errors.permission_denied(self.args.dest))
                    return
                    


        if self.args.force and self.args.interactive and self.args.no_clobber:
            a = ''
            i = ['-i', '--interactive']
            n = ['-n', '--no-clobber']
            f = ['-f', '--force']

            for arg in self.line_args[::-1]:
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
                    self.error(self.errors.permission_denied(path))
                    return
                


        self.args.source.sort()

        # dest = self.args.dest            
        for path in self.args.source:            
            self.move(path)


            # reset the destination if it has been modified (es. in copy_file())
            # self.args.dest = dest

        print()



    def move(self, path: str):



        final_path = self.args.dest
        p = Path(final_path).resolve()

        if os.path.exists(p) and not os.path.isdir(p):
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
                    os.remove(final_path)
                except PermissionError:
                    self.error(self.errors.permission_denied(final_path))
                    return

        dest = shutil.move(path, final_path)

        if self.args.verbose:
            print('%s -> %s' % (path, dest))



