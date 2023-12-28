"""
# `rm`
Remove files and directories
"""

from ...helpers.commands import *
from ...helpers.arguments import Parser

import os
import shutil

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog='rm', description="Remove files and directories")
        self.parser.add_argument('path', nargs="?", help="The file/directory to delete")
        self.parser.add_argument('-f', '--force', action="store_true", help="ignore nonexistent files and arguments, never prompt")
        self.parser.add_argument('-r', '-R', '--recursive', dest="recursive", action="store_true", help="remove directories and their contents recursively")
        self.parser.add_argument('-d', '--dir',action="store_true", help="remove empty directories")
        self.parser.add_argument('-v', '--verbose', action="store_true", help="explain what is being done")


    def run(self):

        if self.args.path:
            if not os.path.exists(self.args.path):
                if not self.args.force:
                    self.error(f"canot access '{self.args.path}': No such file or directory")
                    return
        else:
            self.error("missing operand")
            return
        
        if os.path.isdir(self.args.path) and not (self.args.dir or self.args.recursive):
            self.error(f"cannot remove '{self.args.path}': Is a directory")
            return
        
        if self.args.dir:
            folders = os.listdir(self.args.path or self.info.user.paths.terminal)
            folders = [os.path.abspath(i) for i in folders if os.path.isdir(i)]
            
            for folder in folders:
                if len(os.listdir(folder)) == 0:
                    try:
                        os.rmdir(folder)
                        if self.args.verbose:
                            self.print(f"removing: {folder}")
                    except PermissionError:
                        self.warning(f"cannot open '{folder}': (permission denied)", to_stdout=False)
            self.print()

            

        if self.args.recursive:
            files = []

            if os.path.isfile(self.args.path):
                try:
                    if self.args.verbose:
                        self.print(f"collecting: {self.args.path}")
                    os.remove(self.args.path)
                except PermissionError:
                    self.warning(f"cannot open '{folder}': (permission denied)", to_stdout=False)
            else:
                # Just to show what shutil.rmtree is doing
                for _, _, file in os.walk(self.args.path):
                    files.extend(file)
                    if self.args.verbose:
                        for f in file:
                            self.print(f"collecting: {f}")

                try:
                    if self.args.verbose:
                        self.print(f"deleting {len(files)} files...")
                    shutil.rmtree(os.path.abspath(self.args.path))
                except PermissionError:
                    self.warning(f"cannot open '{folder}': (permission denied)", to_stdout=False)
            self.print()
                

    def close(self):
        if self.args.path and os.path.exists(self.args.path) and os.path.isfile(self.args.path):
            try:
                os.remove(self.args.path)
            except PermissionError:
                if self.status != STATUS_WARN:
                    self.warning(f"cannot open '{self.args.path}': (permission denied)", to_stdout=False)




            