from pathlib import Path
import platform
from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)

class Command(CommandInterface):
    def init(self):
        self.parser = Parser("pwd", description="Print the name of the current working directory")
        self.parser.add_argument("-L", dest='local', action='store_true', default=True, help='print the value of $PWD if it names the current working directory (default: True)')
        self.parser.add_argument("-P", dest='physical', action='store_true', default=True, help='print the physical directory, without any symbolic links')

    def run(self):
        """
        In windows it is harder to read lnk files, so there -P is useless 
        """

        output: Path = Path(self.system.variables.get("$PWD").value)
        if self.args.physical and platform.system() == 'Linux':
            output = output.resolve(True)

        self.print(str(output) + "\n")

        