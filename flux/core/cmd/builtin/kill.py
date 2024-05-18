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
        self.parser.add_argument("pid", help="the pid of the process")
        self.parser.add_argument("-s", dest="sigspec", help="sigspec is a signal name")
        self.parser.add_argument("-n", dest="signum", type=int,  help="signum is a signal number")
        self.parser.add_argument("-l", dest="sigspec", nargs="?", type=int, help="list the signal names;if arguments follow `-l' they are assumed to be signal numbers for which names should be listed")
        self.parser.add_argument("-L", dest="sigspec", nargs="?", type=int, help="synonym for -l")


        self.listed = False

    def setup(self):
        if "-l" in self.command or "-L" in self.command:
            try:
                signum = self.command[self.command.index("-l") + 1 if "-l" in self.command else self.command.index("-L") +1]
                signum = int(signum)

                name = interrupts.event_value_to_name(signum)
                if name:
                    print(name.lstrip("SIG"))
                    return
                else:
                    raise IndexError()
                
            except IndexError:
                table = format.create_adaptive_table([f"{v}) {k}" for k, v in self.system.interrupt_handler.supported.items()])
                print(table)
            
            return

        super().setup()

    def run(self):

        if self.listed:
            return

