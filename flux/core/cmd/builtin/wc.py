import os
from flux.core.helpers.commands import *

class Command(CommandInterface):
    def init(self):
        self.parser = Parser("wc", description="Print newline, word, and byte counts for each FILE.")
        self.parser.add_argument("file", metavar="FILE", nargs="?", help="the FILE to read form (With no FILE, or when FILE is -, read standard input.)")
        self.parser.add_argument("-c", "--bytes", action="store_true", help="print the byte counts")
        self.parser.add_argument("-m", "--chars", action="store_true", help="print the charachter counts")
        self.parser.add_argument("-l", "--lines", action="store_true", help="print the newline counts")
        self.parser.add_argument("-w", "--words", action="store_true", help="print the newline counts")

    def run(self):

        if self.args.file and not os.path.exists(self.args.file):
            self.error(self.errors.file_not_found(self.args.file))
            return
        elif self.args.file and not os.path.isfile(self.args.file):
            self.error(self.errors.cannot_read_dir(self.args.file))
            return

        file = open(self.args.file, 'r') if self.args.file else self.stdin
        contents = file.read().strip().strip("\n")
        output = ""
        if self.parser.no_args:
            self.args.lines = True
            self.args.words = True
            self.args.bytes = True

        if self.args.lines:
            output += f"    {len(contents.splitlines(keepends=False))}"

        if self.args.words:
            output += f"    {len(contents.split())}"

        if self.args.bytes:
            output += f"    {len(contents.encode("utf-8"))}"

        if self.args.file:
            output += " " + self.args.file
        self.print(output)


