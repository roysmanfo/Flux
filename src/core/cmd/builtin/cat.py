from ...helpers.commands import *
from ...helpers.arguments import Parser
import os
import chardet


class Command(CommandInterface):
    def init(self):
        self.parser = Parser("cat", add_help=True, description="Concatenate FILE(s) to standard output")
        self.parser.add_argument("files", nargs="+", help="the files to read (when is -, read standard input)")
        self.parser.add_argument("-A", "--show-all", action="store_true", help="equivalent to -vET")
        self.parser.add_argument("-b", action="store_true", help="number nonempty output lines, overrides -n")
        self.parser.add_argument("-e", action="store_true", help="equivalent to -vE")
        self.parser.add_argument("-E", "--show-ends", action="store_true", help="display $ at end of each line")
        self.parser.add_argument("-n", "--number", action="store_true", help="number all output lines")
        self.parser.add_argument("-s", "--squeeze-blank", action="store_true", help="suppress repeated empty output lines")
        self.parser.add_argument("-t", action="store_true", help="equivalent to -vT")
        self.parser.add_argument("-T", "--show-tabs", action="store_true", help="display TAB characters as ^I")
        self.parser.add_argument("-v", "--show-nonprinting", action="store_true", help="use ^ and M- notation, except for LFD and TAB")

    def setup(self):
        super().setup()

        if self.args.show_all:
            self.args.e = True
            self.args.t = True

        if self.args.b:
            self.args.n = False

        if self.args.e:
            self.args.show_ends = True
            self.args.show_nonprinting = True

        if self.args.t:
            self.args.show_tabs = True
            self.args.show_nonprinting = True

    def run(self):
        for file in self.args.files:
            file: str

            if file != '-':
                if not os.path.exists(file):
                    self.error(self.logger.file_not_found(file))
                    continue

                if os.path.isdir(file):
                    self.error(self.logger.cannot_read_dir(file))
                    continue


            if file == '-':
                lines: list[str] = []
                inp = ''
                while not inp is None:
                    inp = self.input()
                    lines.append(inp)
                print()

                lines =  [i.removesuffix('\n') for i in lines[:-1]] # Also remove trailing None from the list

            else:
                with open(file, 'rb') as f:
                    if not f.readable():
                        self.error(self.logger.permission_denied(file))
                        return
                    
                    content = f.read()
                    enc = "utf-8" if content.strip() == b"" else chardet.detect(content)["encoding"]

                    if not enc:
                        self.error(f"could not determine the encoding of `{file}`")
                        return

                with open(file, 'r', encoding=enc) as f:
                    lines = [i.removesuffix('\n') for i in f.readlines()]

            
            if self.args.show_tabs:
                lines = [i.replace("\t", "^I") for i in f.readlines()]

            if self.args.squeeze_blank:
                r = []
                for l in lines:
                    if l.strip() == '':
                        if l is lines[-1]:
                            r.append(l)
                        elif not lines[lines.index(l) + 1].strip() == '':
                            r.append(l)
                    else:
                        r.append(l)

                lines = r

            if self.args.show_ends:
                lines = [i + '$' for i in lines]

            if self.args.number:
                longest = len(str(len(lines)))
                lines = [f"  {' ' * (longest - len(str(i)))}{i}  {v}" for i, v in enumerate(lines, 1)]

            if self.args.b:
                r = lines.copy()
                longest = len(str(len(lines)))
                i = 1
                for l in lines:
                    if l.strip() != '':
                        r.append(f"  {' ' * (longest - len(str(i)))}{i}  {l}")
                        i += 1
                    else:
                        r.append(f"  {' ' * (longest)}  {l}")

                lines = r

            self.print("\n".join(lines))

            if len(lines) > 0 and (not lines[-1].endswith("\n") or not lines[-1] == ""):
                self.print()
