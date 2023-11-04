"""
# `zip`
Zip stores files in zip archives.
"""

from ...helpers.commands import *
from ...helpers.arguments import Parser

import zipfile
import os

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog='zip', description="Zip stores files in zip archives", add_help=True)
        self.parser.add_argument("archive_name", help="the name of the new archive")
        self.parser.add_argument("files", nargs='+', help="the name of the new archive")


    def run(self):
        
        self.args.files = sorted(self.args.files)

        for file in self.args.files:
            file = str(os.path.abspath(file))
            if not os.path.exists(file):
                self.error(f"cannot access '{file}': No such file or directory")
                return
            
        # * With single files use zipfile
        try:
            with zipfile.ZipFile(f'{self.args.archive_name}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in self.args.files:
                    self.print(f"adding: {file}")
                    if os.path.isdir(file):
                        self.compress_folder(file, zipf)
                    else:
                        self.compress_file(file, zipf)
        except PermissionError:
            self.error(f"cannot open '{file}': (permission denied)")
            os.remove(f'{self.args.archive_name}.zip')
            return
        
        self.print()

    @staticmethod
    def compress_folder(path: str, ziph: zipfile.ZipFile):
        #  ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), 
                        os.path.relpath(os.path.join(root, file), 
                                        os.path.join(path, '..')))
                
    @staticmethod
    def compress_file(filename: str, ziph: zipfile.ZipFile):
        #  ziph is zipfile handle
        ziph.write(filename, filename)