import os
from flux.core.helpers.commands import *
from flux.utils import format

class Command(CommandInterface):
    def init(self):
        self.parser = Parser("wc", description="Print newline, word, and byte counts for each FILE.")
        self.parser.add_argument("files", metavar="FILE", nargs="*", default=["-"], help="the FILE to read form (With no FILE, or when FILE is -, read standard input.)")
        self.parser.add_argument("-c", "--bytes", action="store_true", help="print the byte counts")
        self.parser.add_argument("-m", "--chars", action="store_true", help="print the charachter counts")
        self.parser.add_argument("-l", "--lines", action="store_true", help="print the newline counts")
        self.parser.add_argument("-w", "--words", action="store_true", help="print the newline counts")

    def run(self):
        outputs: list[str] = []
        add_filename = len(self.args.files) > 0
        add_total = len(self.args.files) > 1
        
        for file in self.args.files:
            outputs.append(self.create_output_for_file(file, add_filename=add_filename))
        
        if add_total:
            total = [0 for _ in range(len(outputs[0]) - 1)]
            for file in outputs:
                for index, value in enumerate(file[:-1]):
                    total[index] += value

            total.append("total")
            outputs.append(tuple(total))

        cols = ["" for _ in range(len(outputs[0]))]
        table = format.create_table(cols, contents=outputs, show_headers=False)
        self.print(table.rstrip("\n"))

    
    def create_output_for_file(self, file_path: str, add_filename: bool = False) -> Tuple[str]:
        if file_path:
            self.errors.value = file_path

            if file_path == "-":
                file_path = None # <- read from the standard input

            elif file_path and not os.path.exists(file_path):
                raise RuntimeError(self.errors.file_not_found())
            elif file_path and not os.path.isfile(file_path):
                raise RuntimeError(self.errors.cannot_read_dir())

        file = open(file_path, 'r') if file_path else self.stdin

        if file_path:
            contents = file.read()
        else:
            if not self.recv_from_pipe:
                file_path = "stdin"
            contents = ""

            while (inp := self.input()) != None:
                contents += inp
        contents = contents.strip().strip("\n")
        
        output = []
        if self.parser.no_args:
            self.args.lines = True
            self.args.words = True
            self.args.bytes = True

        if self.args.lines:
            output.append(len(contents.splitlines(keepends=True)))

        if self.args.words:
            output.append(len(contents.split()))

        if self.args.bytes:
            output.append(len(contents.encode("utf-8")))

        if self.args.chars:
            output.append(len(contents))

        if file and add_filename and file_path:
            output.append(file_path)

        return tuple(output)


