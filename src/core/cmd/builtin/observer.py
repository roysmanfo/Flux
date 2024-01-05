"""
# `observer`

### Copyright notice

This files contains work from Kalle Hallden
https://github.com/KalleHallden/desktop_cleaner

MIT License

Copyright (c) 2019 kalle hallden

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json
import os
import shutil
from pathlib import Path
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirModifiedEvent
from ...helpers.arguments import Parser
from ...helpers.commands import CommandInterface
from src import utils


extension_paths = {}
class Command(CommandInterface):

    def init(self) -> None:
        self.parser = Parser(prog="observer", add_help=False)
        self.parser.add_argument("-p", "--path", action="store_true")
        self.parser.add_argument("-a", "--add", nargs=2)
        self.parser.add_argument("-l", "--list", action="store_true")
        self.parser.add_argument("-r", "--remove",)
        self.parser.add_argument("-u", "--update", nargs=2)
        self.parser.add_help_message("""Scans the bucket folder and sorts files in the destination folder
               
usage: observer [-h] [-l] [-p] [-a [.]EXT DEST] [-u [.]EXT DEST] 
                                    
options:
-h, --help                  show this help message and exit
-a, --add [.]EXT DEST       add a new filetype
-l, --list                  list all filetypes controlled
-r, --remove [.]EXT         remove a filetype from the controlled ones
-u, --update [.]EXT DEST    update the value of a filetype
-p, --path                  reveal the bucket's paths:
                                - bucket: Where this command will look for new files
                                - destination: Where the files will be sorted
""")

    def setup(self):
        global extension_paths
        super().setup()

        self.jokes: list[str] = []
        jpath = os.path.join(self.info.syspaths.LOCAL_FOLDER, "observer", "extensions.json")
        self.ext_path = jpath
        try:
            with open(jpath) as f:
                extension_paths = json.load(f)
        
        except FileNotFoundError:
            os.makedirs(os.path.dirname(jpath), exist_ok=True) # exists_ok=True in case just the file is missing
            with open(jpath, "w") as f:
                extension_paths = EXTENSIONS
                json.dump(extension_paths, f, indent=4, sort_keys=True)
            
        except PermissionError:
            self.error(self.logger.permission_denied(jpath))
            self.parser.exit_execution = True

    def run(self) -> None:

        if self.args.help:
            self.parser.help()
            return
        
        if self.args.list:
            self.list_filetypes()
            return
        
        if self.args.add:
            self.add_filetype()
            return

        if self.args.update:
            self.update_filetype()
            return
     
        if self.args.remove:
            self.remove_filetype()
            return

        if self.args.path:
            self.show_path()
            return

        if self.IS_PROCESS:
            self.print("Running observer in background...\n")

        self.sort_files()

    def list_filetypes(self):
        self.print(utils.format.create_adaptive_table("extension", "destination", contents=list(extension_paths.items())))

    def remove_filetype(self):
        ext = str(self.args.remove)
    
        if not ext.startswith("."):
            ext = '.' + ext # or simply  `ext = str(ext[::-1] + '.')[::-1]`

        if not extension_paths.get(ext):
            self.warning("the filetype selected is not being monitored")
            return

        extension_paths.pop(ext)

        try:
            with open(self.ext_path, "w") as f:            
                json.dump(extension_paths, f, indent=4, sort_keys=True)

            self.print(f"filetype '{ext}' removed")

        except PermissionError:
            self.error(self.logger.permission_denied(self.ext_path))

        except FileNotFoundError:
            self.error(self.logger.file_not_found(self.ext_path))

    def add_filetype(self):
        new_ext, dest = [str(i) for i in self.args.add]
    
        if not new_ext.startswith("."):
            new_ext = '.' + new_ext # or simply  `new_ext = str(new_ext[::-1] + '.')[::-1]`

        if extension_paths.get(new_ext):
            self.warning("the filetype selected is already being monitored, use -u to update it")
            return

        extension_paths.update({new_ext: dest})

        try:
            with open(self.ext_path, "w") as f:            
                json.dump(extension_paths, f, indent=4, sort_keys=True)

            self.print(f"filetype '{new_ext}' added")

        except PermissionError:
            self.error(self.logger.permission_denied(self.ext_path))

        except FileNotFoundError:
            self.error(self.logger.file_not_found(self.ext_path))
    
    def update_filetype(self):
        ext, dest = [str(i) for i in self.args.update]
    
        if not ext.startswith("."):
            ext = '.' + ext # or simply  `ext = str(ext[::-1] + '.')[::-1]`

        if not extension_paths.get(ext):
            self.error("the filetype selected is not being monitored, use -a to add it")
            return

        extension_paths.update({ext: dest})
        
        try:
            with open(self.ext_path, "w") as f:            
                json.dump(extension_paths, f, indent=4, sort_keys=True)

            self.print(f"filetype '{ext}' uptated to point '{dest}'")

        except PermissionError:
            self.error(self.logger.permission_denied(self.ext_path))

        except FileNotFoundError:
            self.error(self.logger.file_not_found(self.ext_path))

    def show_path(self) -> bool:
        self.print(f"Bucket:{self.info.user.paths.bucket}")
        self.print(f"Destination:{self.info.user.paths.bucket_destination}\n")
        return False

    def sort_files(self, forever: bool = False) -> None:
        watch_path = Path(self.info.user.paths.bucket)
        destination_root = Path(self.info.user.paths.bucket_destination)

        try:
            os.makedirs(watch_path)
        except FileExistsError:
            pass

        try:
            os.makedirs(destination_root)
        except FileExistsError:
            pass

        try:
            event_handler = self.EventHandler(
                watch_path=watch_path, destination_root=destination_root)

            observer = Observer()
            observer.schedule(event_handler, f'{watch_path}', recursive=True)

            try:
                print(observer.is_alive())
                observer.start()
            except RuntimeError:
                self.error("could not start observer")
                return

            event_handler.on_modified(DirModifiedEvent)

            # Check if we decided to run the process as a background task
            if self.IS_PROCESS:

                try:
                    while not self.info.exit:
                        time.sleep(.1)

                    observer.stop()
                except Exception as e:
                    observer.stop()
                    self.warning(e)
                    return
            else:
                time.sleep(1)
                observer.stop()

            # End the process
            observer.join()
            return

        except FileNotFoundError:
            # We deleted one or both directories
            self.sort_files(forever)

    class EventHandler(FileSystemEventHandler):
        """    
        When a file is moved in the bucket, the event handler detects it and
        moves it in the appropiate folder
        """

        def __init__(self, watch_path: Path, destination_root: Path) -> None:
            self.watch_path = watch_path.resolve()
            self.destination_root = destination_root.resolve()

        @staticmethod
        def create_destination_path(path: Path) -> Path:
            """
            Helper function that adds current year/month to destination path. If the path
            doesn't already exist, it is created.
            :param Path path: destination root to append subdirectories based on date
            """
            path.mkdir(parents=True, exist_ok=True)
            return path

        @staticmethod
        def rename_file(source: Path, destination_path: Path) -> Path:
            """
            Helper function that renames file to reflect new path. If a file of the same
            name already exists in the destination folder, the file name is numbered and
            incremented until the filename is unique (prevents overwriting files).
            :param Path source: source of file to be moved
            :param Path destination_path: path to destination directory
            """
            if Path(destination_path / source.name).exists():
                increment = 0

                while True:
                    increment += 1
                    new_name = destination_path / \
                        f'{source.stem}_{increment}{source.suffix}'

                    if not new_name.exists():
                        return new_name
            else:
                return destination_path / source.name

        def restore_dirs(self) -> None:
            """    
            Will restore the bucket if it has been deleted after opening the app
            """
            try:
                os.makedirs(self.watch_path)
            except:
                pass

            try:
                os.makedirs(self.destination_root)
            except:
                pass

        def on_modified(self, event) -> None:
            self.restore_dirs()

            for child in self.watch_path.iterdir():

                # skips directories and non-specified extensions
                if child.is_file() and child.suffix.lower() in extension_paths:
                    destination_path = self.destination_root / \
                        extension_paths[child.suffix.lower()]
                    destination_path = self.create_destination_path(
                        destination_path)
                    destination_path = self.rename_file(
                        child, destination_path)
                    shutil.move(src=child, dst=destination_path)

                elif child.is_file() and child.suffix.lower() not in extension_paths:
                    destination_path = self.destination_root / \
                        extension_paths["noname"]
                    destination_path = self.create_destination_path(
                        destination_path)
                    destination_path = self.rename_file(
                        child, destination_path)
                    shutil.move(src=child, dst=destination_path)

# TODO: Not store extensions here but add an alternative method to restore externsions.json 
EXTENSIONS = {
    # No name
    'noname':  'other/uncategorized',
    # audio
    '.aif':    'media/audio',
    '.cda':    'media/audio',
    '.mid':    'media/audio',
    '.midi':   'media/audio',
    '.mp3':    'media/audio',
    '.mpa':    'media/audio',
    '.ogg':    'media/audio',
    '.wav':    'media/audio',
    '.wma':    'media/audio',
    '.wpl':    'media/audio',
    '.m3u':    'media/audio',
    # text
    '.txt':    'text/text_files',
    '.doc':    'text/microsoft/word',
    '.docx':   'text/microsoft/word',
    '.odt ':   'text/text_files',
    '.pdf':    'text/pdf',
    '.rtf':    'text/text_files',
    '.tex':    'text/text_files',
    '.wks ':   'text/text_files',
    '.wps':    'text/text_files',
    '.wpd':    'text/text_files',
    # video
    '.3g2':    'media/video',
    '.3gp':    'media/video',
    '.avi':    'media/video',
    '.flv':    'media/video',
    '.h264':   'media/video',
    '.m4v':    'media/video',
    '.mkv':    'media/video',
    '.mov':    'media/video',
    '.mp4':    'media/video',
    '.mpg':    'media/video',
    '.mpeg':   'media/video',
    '.rm':     'media/video',
    '.swf':    'media/video',
    '.vob':    'media/video',
    '.wmv':    'media/video',
    # images
    '.ai':     'media/images',
    '.bmp':    'media/images',
    '.gif':    'media/images',
    '.jpg':    'media/images',
    '.jpeg':   'media/images',
    '.png':    'media/images',
    '.ps':     'media/images',
    '.psd':    'media/images',
    '.svg':    'media/images',
    '.tif':    'media/images',
    '.tiff':   'media/images',
    '.cr2':    'media/images',
    # internet
    '.asp':    'other/internet',
    '.aspx':   'other/internet',
    '.cer':    'other/internet',
    '.cfm':    'other/internet',
    '.cgi':    'other/internet',
    '.pl':     'other/internet',
    '.css':    'other/internet',
    '.htm':    'other/internet',
    '.js':     'other/internet',
    '.jsp':    'other/internet',
    '.part':   'other/internet',
    '.php':    'other/internet',
    '.rss':    'other/internet',
    '.xhtml':  'other/internet',
    '.html':   'other/internet',
    # compressed
    '.7z':     'other/compressed',
    '.arj':    'other/compressed',
    '.deb':    'other/compressed',
    '.pkg':    'other/compressed',
    '.rar':    'other/compressed',
    '.rpm':    'other/compressed',
    '.tar.gz': 'other/compressed',
    '.z':      'other/compressed',
    '.zip':    'other/compressed',
    # disc
    '.bin':    'other/disc',
    '.dmg':    'other/disc',
    '.iso':    'other/disc',
    '.toast':  'other/disc',
    '.vcd':    'other/disc',
    # data
    '.csv':    'programming/database',
    '.dat':    'programming/database',
    '.db':     'programming/database',
    '.dbf':    'programming/database',
    '.log':    'programming/database',
    '.mdb':    'programming/database',
    '.sav':    'programming/database',
    '.sql':    'programming/database',
    '.tar':    'programming/database',
    '.xml':    'programming/database',
    '.json':   'programming/database',
    # executables
    '.apk':    'other/executables',
    '.bat':    'other/executables',
    '.com':    'other/executables',
    '.exe':    'other/executables',
    '.gadget': 'other/executables',
    '.jar':    'other/executables',
    '.wsf':    'other/executables',
    # fonts
    '.fnt':    'other/fonts',
    '.fon':    'other/fonts',
    '.otf':    'other/fonts',
    '.ttf':    'other/fonts',
    # presentations
    '.key':    'text/presentations',
    '.odp':    'text/presentations',
    '.pps':    'text/presentations',
    '.ppt':    'text/presentations',
    '.pptx':   'text/presentations',
    # programming
    '.c':      'programming/c&c++',
    '.class':  'programming/java',
    '.java':   'programming/java',
    '.py':     'programming/python',
    '.sh':     'programming/shell',
    '.h':      'programming/c&c++',
    # spreadsheets
    '.ods':    'text/microsoft/excel',
    '.xlr':    'text/microsoft/excel',
    '.xls':    'text/microsoft/excel',
    '.xlsx':   'text/microsoft/excel',
    # system
    '.bak':    'text/other/system',
    '.cab':    'text/other/system',
    '.cfg':    'text/other/system',
    '.cpl':    'text/other/system',
    '.cur':    'text/other/system',
    '.dll':    'text/other/system',
    '.dmp':    'text/other/system',
    '.drv':    'text/other/system',
    '.icns':   'text/other/system',
    '.ico':    'text/other/system',
    '.ini':    'text/other/system',
    '.lnk':    'text/other/system',
    '.msi':    'text/other/system',
    '.sys':    'text/other/system',
    '.tmp':    'text/other/system'
}
