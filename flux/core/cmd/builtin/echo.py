from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)


class Command(CommandInterface): 
    def init(self):
        self.parser = Parser(prog="echo", description="display a line of text", usage="echo [SHORT-OPTION]... [STRING]...")
        self.parser.add_argument("string", nargs="*", help="the text to display")
        self.parser.add_argument("-n", action="store_true", help="do not output the trailing newline")
        self.parser.add_argument("-e", action="store_true", help="enable interpretation of backslash escapes")
        
        self.parser.add_argument("-E", action="store_true", default=True, help="disable interpretation of backslash escapes (default)")
        # ^^^ not actually needed ^^^

    def run(self):
        string = " ".join(self.args.string)

        if self.args.e:
            string = string.encode('utf-8').decode('unicode_escape')

        self.print(string, end="\n" if not self.args.n else "")
        self.print()
