from flux.core.interfaces.commands import (
    CommandInterface,
    Parser
)

import os
from pathlib import Path
import base64
import binascii


ENTRY_POINT = 'Base64'
DEFAULT_COLS = 76

class Base64(CommandInterface):
    def init(self):
        self.parser = Parser('base64', description='Base64 encode or decode FILE, or standard input, to standard output.')
        self.parser.add_argument("FILE", nargs='*', help='With no FILE, or when FILE is -, read standard input.')
        self.parser.add_argument('-d', '--decode', action='store_true', help='decode data')
        self.parser.add_argument('-v', '--validate', action='store_true', help='check if the data to be decoded is in the correct format (default: false)')
        self.parser.add_argument('-w', '--wrap', nargs='...', dest='cols', metavar="COLS", type=int, help=f'wrap encoded lines after COLS character (default {DEFAULT_COLS}).')


    def run(self):
        if not (content := self.read_input()):
            return

        if self.args.decode:
            try:
                self.print(base64.b64decode(content, validate=self.args.validate).decode())
            except binascii.Error as e:
                self.error(f'invalid input: {e}')
        else:
            import textwrap
            encoded = base64.b64encode(content).decode()
            if self.args.cols is not None:
                width = self.args.cols[0] if len(self.args.cols) > 0 else DEFAULT_COLS
                wrapped = '\n'.join(textwrap.wrap(encoded, width))
                self.print(wrapped)
            else:
                self.print(encoded)

    def read_input(self) -> bytes | None:
        file = self.args.FILE[0] if self.args.FILE else '-'
        if file == "-":
            content = inp = ''
            while inp is not None:
                inp = self.input()

                if inp is not None:
                    content += inp
            return content.encode()
        
        else:
            file_path = Path(os.path.realpath(file)).resolve()

            if not file_path.exists():
                self.error(self.errors.file_not_found(str(file_path)))
                return None

            if not file_path.is_file():
                self.error(self.errors.cannot_read_dir(str(file_path)))
                return None            

            try:
                with open(file_path, 'rb') as r:
                    return r.read()

            except PermissionError:
                self.error(self.errors.permission_denied(str(file_path)))
                self.error(f'An error occurred while reading {str(file_path)}\n{e}')

            except Exception as e:
                self.error(f'An error accoured while reading {str(file_path)}\n{e}')
                return None
