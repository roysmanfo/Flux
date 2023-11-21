import os
from ...helpers.arguments import Parser
from ...helpers.commands import *


class Command(CommandInterface):

    def init(self):
        self.parser = Parser(
            "head", description="Print the first 10 lines of each FILE to standard output. With more than one FILE, precede each with a header giving the file name.")

        self.parser.add_argument("file", nargs="*", help="the files to display; With no FILE, or when FILE is -, read standard input.")
        self.parser.add_argument("-c", "--bytes", type=int, help="print the first NUM bytes of each file")
        self.parser.add_argument("-n", "--lines", default=10, type=int, help="print the first NUM lines instead of the first 10")
        self.parser.add_argument("-z", "--zero-terminated", help="line delimiter is NUL, not newline")

    def setup(self):
        super().setup()



    def run(self):
        self.args.file: list[str]

        if len(self.args.file) == 0:
            content = self.input()
            
            if content is None:
                return
            
            content = self.format_str(content)
        else:
            for file in self.args.file:
                self.logger.value = file
                content = ""

                if not os.path.exists(file) and file:
                    self.error(self.logger.file_not_found())
                    continue
                
                if os.path.isdir(file):
                    self.error(self.logger.cannot_read_dir())
                    continue

                try:
                    with open(file, "r") as f:
                        content = f.read()

                except PermissionError:
                    self.error(self.logger.permission_denied())
                    

        
    def format_str(self, content: str) -> list[str] : 
        if self.args.bytes:
            content = content[:self.args.bytes]
            content = content.splitlines(keepends=True)

        else:
            content = content.splitlines(keepends=True)
            content = content[:self.args.lines]

        if self.args.zero_terminated:
            content = [i.replace("\n", "NUL") for i in content]

        return content