"""
# `unzip`
Decompress files from zip archives.
"""

from flux.core.helpers.commands import *
from flux.core.helpers.arguments import Parser
from flux.utils import format

import os
import zipfile

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog='unzip', description="Extracts files from compressed zip archives")
        self.parser.add_argument("archive_name", help="the name of the zip archive (you can omit the .zip extension)")
        self.parser.add_argument("-d", dest="destination", metavar="exdir", default=".", help="extract files into exdir (default: current directory)")
        self.parser.add_argument("-l", action="store_true", help="list files (short format)")
        self.parser.add_argument("-x", dest="xlist", metavar="xlist", nargs="+", help="exclude files that follow (in xlist)")


    def run(self):        
        
        try:
            self.args.archive_name = self._normalize_archive_name(self.args.archive_name)
        except ValueError as e:
            self.error(str(e))
            return

        if not os.path.exists(self.args.destination):
            try:
                os.makedirs(self.args.destination, mode=777, exist_ok=True)
            except PermissionError:
                self.error(f"cannot create '{self.args.destination}': (permission denied)")
                return
        
        
        if self.args.l:
            self.list_files(self.args.archive_name)
            return
        
        self.extract_archive(self.args.archive_name, self.args.destination)


    def _normalize_archive_name(self, path: str) -> str:

        def try_to_open(archive_path: str) -> bool:
            try:
                archive = zipfile.ZipFile(archive_path, "r")
                archive.close()
                return True
            except:
                return False

        if not os.path.exists(path) or not try_to_open(path):
            attempts: List[str] = [path]
            
            if not path.endswith(".zip"):
                path +=  ".zip"

            if not os.path.exists(path) or not try_to_open(path):
                attempts.append(path)
                path = path.removesuffix(".zip") + ".ZIP"

                if not os.path.exists(path) or not try_to_open(path):
                    attempts.append(path)
                    raise ValueError(f"cannot find or open {attempts[0]}, {attempts[1]} or {attempts[2]}.")

        return path

    def list_files(self, archive_name: str) -> None:
        with zipfile.ZipFile(archive_name, 'r') as zip_ref:
            # read file info
            file_info = [zip_ref.getinfo(file) for file in zip_ref.namelist()]
            file_info = [
                (
                    file.file_size,                                    # Length
                    "-".join(str(i) for i in file.date_time[:3]),      # Date
                    ":".join(str(i) for i in file.date_time[3:-1]),    # Time
                    file.filename                                      # Name
                ) for file in file_info
            ]

            # add total
            total_len = sum(file[0] for file in file_info)
            num_files = len(file_info)
            file_info.append(("-" * len(str(total_len)), "", "", "-" * len(f"{num_files} files")))
            file_info.append((total_len, "", "", f"{num_files} files"))

            # create table
            table = format.create_table("Length", "Date", "Time", "Name", contents=file_info).rstrip("\n")
            self.print(table)


    def extract_archive(self, archive_name: str, destination: str) -> None:
        with zipfile.ZipFile(archive_name, 'r') as zip_ref:
            # Get the list of items in the archive
            archive_items = zip_ref.namelist()

            for item in archive_items:


                # Ensure the item's path separator is consistent (use forward slash)
                item = item.replace('\\', '/')

                # Extract the item name (file or directory) without the path
                item_name = os.path.basename(item)
                
                
                # ignore this file if it is in xlist
                if self.args.xlist and item in self.args.xlist:
                    continue

                # Check if the item is a directory
                is_directory = item.endswith('/')

                if is_directory:
                    # Handle directory extraction
                    dest_dir = os.path.join(destination, item_name)

                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)

                else:
                    # Handle file extraction
                    dest_path = os.path.join(destination, item_name)

                    # Check for file conflicts and rename if necessary
                    count = 1
                    base_name, ext = os.path.splitext(item_name)
                    while os.path.exists(dest_path):
                        new_name = f"{base_name} ({count}){ext}"
                        dest_path = os.path.join(destination, new_name)
                        count += 1

                    with zip_ref.open(item) as source, open(dest_path, 'wb') as dest:
                        dest.write(source.read())
