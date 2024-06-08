from ...helpers.arguments import Parser
from ...helpers.commands import *

from flux.utils import format
from flux.core.system import interrupts

class Command(CommandInterface):
    def init(self):
        description = "Send the processes identified by PID " \
                      "the signal named by SIGSPEC or SIGNUM. " \
                      "If neither SIGSPEC nor SIGNUM is present, then SIGTERM is assumed."
        self.parser = Parser("kill", description=description)
        self.parser.add_argument("pid", nargs="?", type=int, help="the pid of the process")
        self.parser.add_argument("-s", dest="sigspec", help="sigspec is a signal name")
        self.parser.add_argument("-n", dest="signum", type=int,  help="signum is a signal number")
        self.parser.add_argument("-l", dest="sigspec", nargs="?", type=int, help="list the signal names;if arguments follow `-l' they are assumed to be signal numbers for which names should be listed")
        self.parser.add_argument("-L", dest="sigspec", nargs="?", type=int, help="synonym for -l")


        self.listed = False

    def setup(self):
        super().setup()
        
        if "-l" in self.command or "-L" in self.command:
            self.listed = True
            try:
                signum = self.command[self.command.index("-l") + 1 if "-l" in self.command else self.command.index("-L") +1]
                signum = int(signum)

                name = interrupts.event_value_to_name(signum)
                if name:
                    self.print(name.lstrip("SIG"))
                    return
                else:
                    raise IndexError()
                
            except IndexError:
                table = format.create_adaptive_table([f"{v}) {k}" for k, v in self.system.interrupt_handler.supported.items()])
                self.print(table)
            
            return


    def run(self):
        if self.listed:
            return

        signum = interrupts.event_name_to_value("SIGTERM")

        if self.args.sigspec:
            signum = interrupts.event_name_to_value(self.args.sigspec)
        elif self.args.signum:
            signum = self.args.signum

        if not signum:
            self.error(f"{signum}: invalid signal specification")
            return
        
        if not self.system.processes.find(self.args.pid):
            self.error(self.parser.format_usage().rstrip("\n"))
            return
        
        proc = self.system.processes.remove(self.args.pid)
        print(proc)


