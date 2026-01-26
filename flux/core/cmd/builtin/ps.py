"""
# `ps`
Allows to view running Flux processes
"""

from flux.core.interfaces.commands import (
    CommandInterface,
    Parser
)
from flux.utils import tables

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


        procceses = self.system.processes.list()

        contents = []
        match self.args.mode:
            case "simple":
                for p in procceses:
                    contents.append([p.id, p.owner, p.name, p.time_alive])
                self.print()
                self.print(tables.create_table("ID", "OWNER", "NAME", "TIME ALIVE", rows=contents), end="")

            case "all":
                contents = []
                for p in procceses:
                    contents.append([p.id, p.ppid, p.owner, p.name, p.native_id, p.time_alive, p.is_reserved_process, " ".join(p.line_args)])
                self.print()
                self.print(tables.create_table("ID", "PPID", "OWNER", "NAME", "NATIVE ID", "TIME ALIVE", "IS RESERVED PROCESS", "ARGS", rows=contents), end="")

            case "threads":
                contents = []
                for p in procceses:
                    contents.append([p.id, p.name, p.native_id])

                self.stdout.write(tables.create_table("ID", "NAME", "NATIVE ID", rows=contents))

            case "misc":
                for p in procceses:
                    contents.append([p.id, p.ppid, p.owner, p.name, p.is_reserved_process, p.time_alive])

                self.stdout.write(tables.create_table("ID", "PPID", "OWNER", "NAME", "IS RESERVED PROCESS", "TIME ALIVE", rows=contents))

            case _:
                self.error(self.errors.parameter_not_supported(self.args.mode))
                
