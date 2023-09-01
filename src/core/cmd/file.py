"""
File command
============

This command gives information on a specific file given as argument


Usage: python file.py FILEPATH
  or:  python file.py DIRPATH
  or:  python file.py FILEPATH [args]
```

Opions:
    -m, --metadata              Extracts the metadata of the file if possible.
    -k key, --keys key          Used combined with `-m`, allows to specify a key (can be used multiple times)
"""
from .helpers.commands import *
from .helpers.arguments import Parser
import os
from pathlib import Path
import chardet
from PIL import Image

# from PIL.ExifTags import TAGS

class Command(CommandInterface):
    
    def init(self):
        self.parser = Parser(add_help=True, prog="file", description="Gives information on a specific file given as argument")
        self.parser.add_argument("PATH", help="The path of the file.")
        self.parser.add_argument("-m", "--metadata", help="Extracts the EXIF metadata of the file if possible.", action="store_true")
        self.parser.add_argument("-k", "--keys", help="Used combined with `-m`, allows to filter keys (can be used multiple times)", action="append")

    
    def run(self, command: list[str]):
        self.args = self.parser.parse_args(command[1:])
        
        if self.parser.exit_execution:
            print()
            return

        if not os.path.exists(self.args.PATH):
            self.error(STATUS_ERR, f"cannot open `{self.args.PATH}` (No such file or directory)")
            return
        
        self.args.PATH = Path(self.args.PATH)

        if self.args.metadata:
            info = self.get_metadata(self.args.PATH, self.args.keys)
        else:
            try:
                info = self.file_info(self.args.PATH)
            except PermissionError:
                self.error(STATUS_ERR, f"cannot open `{self.args.PATH}` (permission denied)")
                return

        if info is None:
            self.parser.exit_execution = True
            return

        self.stdout.write(info + "\n\n")


    def file_info(self, filepath: str | Path) -> str:
        """
        Gets file information
        """

        file_stats = os.stat(filepath)
        file_type = ""

        if os.path.islink(filepath):
            file_type += "symbolic link to "
        elif os.path.isfile(filepath):
            file_type += "regular file"
        elif os.path.isdir(filepath):
            file_type += "directory"
        else:
            file_type += "unknown"

        if not os.path.isdir(filepath):
            with open(filepath, 'rb') as file:
                image_ext = ['jpg', 'jpeg', 'tif', 'tif', 'png',
                            'gif', 'bmp', 'webp', 'pdf', 'docx', 'xlsx', 'pptx']
                if str(self.args.PATH).rsplit('.', maxsplit=1)[-1].lower() in image_ext:
                    encoding = ""
                else:
                    encoding: str = ", " + \
                        chardet.detect(file.read())[
                            'encoding'] or ", unknown encoding"
        else:
            encoding = ""
        return f"{filepath}: {file_type}, {oct(file_stats.st_mode)[-3:]}, {file_stats.st_size} bytes{encoding.upper()}"


    def get_metadata(self, path, keys: list = []) -> str | None:
        """
        Retreive metadata from an image file

        ### Supported Types
        - JPEG (.jpg, .jpeg)
        - TIFF (.tif, .tiff)
        - PNG (.png)
        - GIF (.gif)
        - BMP (.bmp)
        - WebP (.webp)
        - PDF (.pdf)
        - Microsoft Office documents (.docx, .xlsx, .pptx)
        """

        accepted = ['jpg', 'jpeg', 'tif', 'tif', 'png', 'gif',
                    'bmp', 'webp', 'pdf', 'docx', 'xlsx', 'pptx']
        acc = ", ".join([i for i in accepted])
        acc.removesuffix(', ')

        if str(path).rsplit('.', maxsplit=1)[-1].lower() not in accepted:
            self.error(STATUS_ERR, f"Operation not supported for this type of file\nTypes suppoted: {acc}")
            return None

        image = Image.open(path)
        metadata = image.info
        if keys:
            filtered_metadata = {k: v for k, v in metadata.items() if k in self.args.keys}
            results = [f"{j}: {image.info[j]}" for _,
                    j in enumerate(filtered_metadata)]
        else:
            keys = image.info.keys()
            results = [f"{j}: {image.info[j]}" for _, j in enumerate(keys)]
        return "\n".join(results)

