"""
# `file`

This command gives information on a specific file given as argument
```txt
Opions:
    -m, --metadata              Extracts the metadata of the file if possible.  
    -k key, --keys key          Used combined with `-m`, allows to specify a key (can be used multiple times)
```
"""
from ...helpers.commands import *
from ...helpers.arguments import Parser
import os
from pathlib import Path
from PIL import Image

# from PIL.ExifTags import TAGS

class Command(CommandInterface):
    
    def init(self):
        self.parser = Parser(add_help=True, prog="file", description="Gives information on a specific file given as an argument")
        self.parser.add_argument("PATH", help="The path of the file.")
        self.parser.add_argument("-m", "--metadata", help="Extracts the EXIF metadata of the file if possible.", action="store_true")
        self.parser.add_argument("-k", "--keys", help="Used combined with `-m`, allows filtering keys (can be used multiple times)", action="append")

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
        file_type = ""
        if os.path.islink(filepath):
            file_type += "symbolic link to "
        elif os.path.isfile(filepath):
            file_type += "regular file"
        elif os.path.isdir(filepath):
            file_type += "directory"
        else:
            file_type += "unknown"

        try:
            file_size = os.path.getsize(filepath)
        except OSError as e:
            self.error(STATUS_ERR, f"Error getting file size: {e}")
            return

        return f"{filepath}: {file_type}, {oct(os.stat(filepath).st_mode)[-3:]}, {file_size} bytes"

    def get_metadata(self, path, keys: list = []) -> str | None:
        """
        Retrieve metadata from an image file

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
        accepted = ['jpg', 'jpeg', 'tif', 'tiff', 'png', 'gif',
                    'bmp', 'webp', 'pdf', 'docx', 'xlsx', 'pptx']
        acc = ", ".join([i for i in accepted])
        acc.removesuffix(', ')

        if str(path).rsplit('.', maxsplit=1)[-1].lower() not in accepted:
            self.error(STATUS_ERR, f"Operation not supported for this type of file\nTypes supported: {acc}")
            return None

        image = Image.open(path)
        metadata = image.info
        if keys:
            filtered_metadata = {k: v for k, v in metadata.items() if k in self.args.keys}
            results = [f"{j}: {image.info[j]}" for _, j in enumerate(filtered_metadata)]
        else:
            keys = image.info.keys()
            results = [f"{j}: {image.info[j]}" for _, j in enumerate(keys)]
        return "\n".join(results)
