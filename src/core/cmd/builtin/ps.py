"""
# `ps`
Allows to view running Flux processes
"""

from ...helpers.commands import *
from ...helpers.arguments import Parser

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog="lp", description="Allows to view running Flux processes", add_help=True)
        self.parser.add_argument("mode", nargs="?", default="simple", help="How to view the processes <(s)imple|(l)ist|(o)utput|(t)hreads|(m)isc|(a)ll>")

    def run(self):
        mapped_modes = {
            's': 'simple',  'simple':   'simple',
            'l': 'list',    'list':     'list',
            'o': 'output',  'output':   'output',
            't': 'threads', 'threads':  'threads',
            'm': 'misc',    'misc':     'misc',
            'a': 'all',     'all':      'all',
        }
        
        self.args.mode = mapped_modes[self.args.mode.lower()]


        procceses = self.info.processes.list()

        if self.parser.exit_execution:
            print()
            return


        if self.args.mode == "all":
            for p in procceses:
                self.stdout.write(p.get_info().__str__() + "\n")

        else:
            for p in procceses:
                self.stdout.write(p.__str__() + "\n")

        self.stdout.write("\n")