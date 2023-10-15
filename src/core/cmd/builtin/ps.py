"""
# `ps`
Allows to view running Flux processes
"""

from ...helpers.commands import *
from ...helpers.arguments import Parser
from src.utils.format import create_adaptive_table

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog="ps", description="Allows to view running Flux processes", add_help=True)
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

        self.args.mode = mapped_modes[self.args.mode.lower()] if self.args.mode in mapped_modes.keys() else None


        procceses = self.info.processes.list()

        contents = []
        if self.args.mode == "all":
            contents = []
            for p in procceses:
                contents.append([p.id, p.owner, p.name, p.native_id, p._calculate_time(time.time() - p.started), " ".join(p.line_args)])

            self.stdout.write(create_adaptive_table("ID", "OWNER", "NAME", "NATIVE ID", "TIME ALIVE", "ARGS", contents=contents))
            
        else:

            for p in procceses:
                contents.append([p.id, p.owner, p.name, p._calculate_time(time.time() - p.started)])

            self.stdout.write(create_adaptive_table("ID", "OWNER", "NAME", "TIME ALIVE", contents=contents))
