from ...helpers.commands import CommandInterface
from ...helpers.arguments import Parser

import shutil

class Command(CommandInterface):
    
    def init(self):
        self.parser = Parser(prog='mv', add_help=True, description='Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.')

        self.parser.add_argument('source', nargs='+', help='the file(s) or directory(s) to copy')
        self.parser.add_argument('dest', help='the destination of the sources')
        self.parser.add_argument('-f', '--force', action='store_true', help='do not prompt before overwriting (overrides a previous -i or -n)')
        self.parser.add_argument('-i', '--interactive', action='store_true', help='prompt before overwrite (overrides a previous -n or -f)')
        self.parser.add_argument('-n', '--no-clobber', action='store_true', help='do not overwrite an existing file (overrides previus -i or -f)')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='explain what is being done')

    def run(self):
        """
        This command tells a random programming joke
        """

                