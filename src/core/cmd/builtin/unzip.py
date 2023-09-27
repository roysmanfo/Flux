"""
# `unzip`
Decompress files from zip archives.
"""

from ...helpers.commands import *
from ...helpers.arguments import Parser

import os
import zipfile

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog='unzip', description="Extracts files from compressed zip archives", add_help=True)
        self.parser.add_argument("archive_name", help="the name of the zip archive (you can omit the .zip extension)")
        self.parser.add_argument("destination", nargs='?', default=".", help="the destination of the extracted data (default: current directory)")
        self.parser.add_argument("-a", "--adapt", action="store_true", help="handle conflicts if the destionation folder already exists")


    def run(self):
        self.args = self.parser.parse_args(self.command[1:])
        
        if self.parser.exit_execution:
            print()
            return
        
        
        if not os.path.exists(self.args.archive_name):
            attempts: list[str] = [self.args.archive_name]
            
            if not self.args.archive_name.endswith(".zip"):
                self.args.archive_name +=  ".zip"

            if not os.path.exists(self.args.archive_name):
                attempts.append(self.args.archive_name)
                self.args.archive_name = self.args.archive_name.removesuffix(".zip") + ".ZIP"

                if not os.path.exists(self.args.archive_name):
                    attempts.append(self.args.archive_name)
                    self.error(STATUS_ERR, f"cannot find or open {attempts[0]}, {attempts[1]} or {attempts[2]}.")
                    return

        if not os.path.exists(self.args.destination):
            try:
                os.makedirs(self.args.destination, mode=777, exist_ok=True)
            except PermissionError:
                self.error(STATUS_ERR, f"cannot create '{self.args.destination}': (permission denied)")
                return
                
        else:
            if self.args.adapt:
                dest = os.path.basename(self.args.destination)
                prefix = os.path.dirname(self.args.destination)
                i = 1
                while os.path.exists(os.path.join(prefix, dest)):
                    dest = f"{dest} ({i})"
                    i += 1
                self.args.destination = os.path.join(prefix, dest)

            else:
                self.error(STATUS_ERR, f"folder '{self.args.destination}' already exists")
                return


        with zipfile.ZipFile(self.args.archive_name, 'r') as zip_ref:
            # Get the list of items in the archive
            archive_items = zip_ref.namelist()

            for item in archive_items:
                # Ensure the item's path separator is consistent (use forward slash)
                item = item.replace('\\', '/')

                # Extract the item name (file or directory) without the path
                item_name = os.path.basename(item)

                # Check if the item is a directory
                is_directory = item.endswith('/')

                if is_directory:
                    # Handle directory extraction
                    dest_dir = os.path.join(self.args.destination, item_name)

                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)

                else:
                    # Handle file extraction
                    dest_path = os.path.join(self.args.destination, item_name)

                    # Check for file conflicts and rename if necessary
                    count = 1
                    base_name, ext = os.path.splitext(item_name)
                    while os.path.exists(dest_path):
                        new_name = f"{base_name} ({count}){ext}"
                        dest_path = os.path.join(self.args.destination, new_name)
                        count += 1

                    with zip_ref.open(item) as source, open(dest_path, 'wb') as dest:
                        dest.write(source.read())
