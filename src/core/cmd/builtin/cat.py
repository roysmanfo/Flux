from ...helpers.commands import *
from ...helpers.arguments import Parser

class Command(CommandInterface):
    def init(self):
        self.parser = Parser("cat", add_help=True, description="Concatenate FILE(s) to standard output")
        self.parser.add_argument("files", nargs="+", help="the files to read (when is -, read standard input)")
        self.parser.add_argument("-A", "--show-all", action="store_true", help="equivalent to -vET")
        self.parser.add_argument("-b", action="store_true", help="number nonempty output lines, overrides -n")
        self.parser.add_argument("-e", "--show-ends", action="store_true", help="equivalent to -vE")
        self.parser.add_argument("-E", "--show-ends", action="store_true", help="display $ at end of each line")
        self.parser.add_argument("-n", "--number", action="store_true", help="number all output lines")
        self.parser.add_argument("-s", "--squeeze-blank", action="store_true", help="suppress repeated empty output lines")
        self.parser.add_argument("-t", action="store_true", help="equivalent to -vT")
        self.parser.add_argument("-T", "--show-tabs", action="store_true", help="display TAB characters as ^I")
        self.parser.add_argument("-v", "--show-nonprinting", action="store_true", help="use ^ and M- notation, except for LFD and TAB")

    def run(self):
        pass
