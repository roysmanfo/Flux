import os
from flux.core.helpers.arguments import Parser
from flux.core.helpers.commands import *


class Command(CommandInterface):

    def init(self):
        self.parser = Parser(
            "tail", description="Print the last 10 lines of each FILE to standard output. With more than one FILE, precede each with a header giving the file name.")

        self.parser.add_argument("file", nargs="*", help="the files to display; With no FILE, or when FILE is -, read standard input.")
        self.parser.add_argument("-c", "--bytes", type=int, help="print the first NUM bytes of each file")
        self.parser.add_argument("-n", "--lines", default=10, type=int, help="print the first NUM lines instead of the first 10")
        self.parser.add_argument("-z", "--zero-terminated", action="store_true", help="line delimiter is NUL, not newline")

    def run(self):
        self.args.file: list[str]

        if len(self.args.file) == 0:
            content = ""
            inp = ""

            while inp is not None:
                inp = self.input()

                if inp is not None:
                    content += inp
            
            self.print() # place a space between stdin and stdout
            
            self.display(self.format_str(content))
        else:
            for file in self.args.file:
                inp = ""
                self.errors.value = file
                content = ""
                
                if file == "-":
                    while inp is not None:
                        inp = self.input()

                        if inp is not None:
                            content += inp
                else:
                    if not os.path.exists(file) and file:
                        self.error(self.errors.file_not_found())
                        continue
                    
                    if os.path.isdir(file):
                        self.error(self.errors.cannot_read_dir())
                        continue

                    try:
                        with open(file, "r") as f:
                            content = f.read()

                    except PermissionError:
                        self.error(self.errors.permission_denied())
                        continue

                self.display(self.format_str(content))
                    

        
    def format_str(self, content: str) -> list[str] : 
        if self.args.bytes:
            content = content[::-1][:self.args.bytes][::-1]
            content = content.splitlines(keepends=True)

        else:
            content = content.splitlines(keepends=True)
            content = content[::-1][:self.args.lines][::-1]

        if self.args.zero_terminated:
            content = [i.replace("\n", "NUL") for i in content]

        return content
    

    def display(self, content: list[str]) -> None:
        for i in content:
            # You may be asking yourself why did I add NUL in the first place
            # Well, idk man
            self.print(i.rstrip("NUL"), end="" if i.endswith("\n") else "\n")
        
        self.print()

