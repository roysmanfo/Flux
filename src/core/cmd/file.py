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

import sys
import os
from pathlib import Path
import argparse
import chardet
from PIL import Image
# from PIL.ExifTags import TAGS
sys.argv.pop(0)
parser = argparse.ArgumentParser()


def get_options():
    """
    Manages options given by user
    """
    parser.add_argument("-m", "--metadata",
                        help="Extracts the metadata of the file if possible.", action="store_true")
    parser.add_argument(
        "-k", "--keys", help="Used combined with `-m`, allows to filter keys (can be used multiple times)", action="append")


def check() -> Path:
    """
    Input validation operations
    """
    validated_path: Path = Path()

    if len(sys.argv) < 1:
        print("No file specified")
        sys.exit(1)

    else:
        for i in sys.argv:
            if os.path.isfile(i) or os.path.isdir(i):
                validated_path = Path(i)

    return validated_path


def file_info(filepath: str | Path) -> str:
    """
    Gets file information
    """

    if not os.path.exists(filepath):
        return "Given path does not exist"

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
            if str(path).rsplit('.', maxsplit=1)[-1].lower() in image_ext:
                encoding = ""
            else:
                encoding: str = ", " + \
                    chardet.detect(file.read())[
                        'encoding'] or ", unknown encoding"
    else:
        encoding = ""
    return f"{filepath}: {file_type}, {oct(file_stats.st_mode)[-3:]}, {file_stats.st_size} bytes{encoding.upper()}"


def get_metadata(path, keys: list = []) -> str:
    """
    Retreive metadata from an image file

    ###Supported Types
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
    acc = "".join([f'{i}, ' for i in accepted])
    acc.removesuffix(', ')

    if str(path).rsplit('.', maxsplit=1)[-1].lower() not in accepted:
        print("Operation not supported for this type of file")
        print(f'Types suppoted: {acc}')
        sys.exit(1)

    image = Image.open(path)
    metadata = image.info
    if keys:
        filtered_metadata = {k: v for k,
                             v in metadata.items() if k in args.keys}
        results = [f"{j}: {image.info[j]}" for _,
                   j in enumerate(filtered_metadata)]
    else:
        keys = image.info.keys()
        results = [f"{j}: {image.info[j]}" for _, j in enumerate(keys)]
    return "\n".join(results)


path = check().resolve()
get_options()
args = parser.parse_args()

if args.metadata:
    info = get_metadata(path, args.keys)
else:
    info = file_info(path)

print(info)
