from ...helpers.arguments import Parser
from ...helpers.commands import *


class Command(CommandInterface):

    def init(self):
        self.parser = Parser(
            "head", description="Print the first 10 lines of each FILE to standard output. With more than one FILE, precede each with a header giving the file name.")

        self.parser.add_argument("file", nargs="*", help="the files to display; With no FILE, or when FILE is -, read standard input.")
        self.parser.add_argument("-c", "--bytes", help="print the first NUM bytes of each file")
        self.parser.add_argument("-n", "--lines", help="print the first NUM lines instead of the first 10")
        self.parser.add_argument("-z", "--zero-terminated", help="line delimiter is NUL, not newline")

    def run(self):
        pass
        