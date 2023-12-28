"""
# `ps`
Allows to view running Flux processes
"""

from ...helpers.commands import *
from ...helpers.arguments import Parser
from src.utils import format

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog="ps", description="Allows to view running Flux processes")
        self.parser.add_argument("mode", nargs="?", default="simple", help="How to view the processes <(s)imple|(t)hreads|(m)isc|(a)ll>")

    def run(self):
        mapped_modes = {
            's': 'simple',  'simple':   'simple',
            't': 'threads', 'threads':  'threads',
            'm': 'misc',    'misc':     'misc',
            'a': 'all',     'all':      'all',
        }

        self.args.mode = mapped_modes[self.args.mode.lower()] if self.args.mode in mapped_modes.keys() else self.args.mode


        procceses = self.info.processes.list()

        contents = []
        match self.args.mode:
            case "simple":
                for p in procceses:
                    contents.append([p.id, p.owner, p.name, p.time_alive])
                self.print()
                self.print(format.create_adaptive_table("ID", "OWNER", "NAME", "TIME ALIVE", contents=contents), end="")

            case "all":
                contents = []
                for p in procceses:
                    contents.append([p.id, p.pid, p.owner, p.name, p.native_id, p.time_alive, p.is_reserved_process, " ".join(p.line_args)])
                self.print()
                self.print(format.create_adaptive_table("ID", "PID", "OWNER", "NAME", "NATIVE ID", "TIME ALIVE", "IS RESERVED PROCESS", "ARGS", contents=contents), end="")

            case "threads":
                contents = []
                for p in procceses:
                    contents.append([p.id, p.name, p.native_id])

                self.stdout.write(format.create_adaptive_table("ID", "NAME", "NATIVE ID", contents=contents))

            case "misc":
                for p in procceses:
                    contents.append([p.id, p.pid, p.owner, p.name, p.is_reserved_process, p.time_alive])

                self.stdout.write(format.create_adaptive_table("ID", "PID", "OWNER", "NAME", "IS RESERVED PROCESS", "TIME ALIVE", contents=contents))

            case _:
                self.error(self.logger.parameter_not_supported(self.args.mode))
                
