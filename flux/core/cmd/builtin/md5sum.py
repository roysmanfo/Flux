import os
from flux.core.helpers.commands import (
    CommandInterface,
    Parser,
    PreLoadConfigs
)

import hashlib


class Command(CommandInterface):

    PRELOAD_CONFIGS = PreLoadConfigs(prefered_mode_stdin='b')

    def init(self):
        self.parser = Parser('md5sum', description='Print or check MD5 (128-bit) checksums')
        self.parser.add_argument('FILE', nargs='*', help='With no FILE, or when FILE is -, read standard input.')

    def run(self):
        files: list[str] = self.args.FILE

        if not files:
            files = ['-']

        for file_path in files:
            md5 = hashlib.md5()

            if file_path == '-':
                # read stdin
                while (_in := self.input(n=4096)):
                    md5.update(_in)

            else:
                if not os.path.exists(file_path):
                    self.error(self.errors.file_not_found(file_path))
                    continue

                with open(file_path, 'rb') as f:
                    while (_in := f.read(4096)):
                        md5.update(_in)

            self.print(f"{md5.hexdigest()}  {file_path}")
