import subprocess
from ...helpers.commands import *
from ...helpers.arguments import Parser



p: subprocess.Popen = None
class Command(CommandInterface):
    
    def init(self):
        self.parser = Parser("ext", description="Allows to use commands from outside flux")
        self.parser.add_argument("command", action="append", help="the command to run")

    def setup(self):
        if "-h" in self.command or "--help" in self.command:
            super().setup()

        elif len(self.command[1:]) == 0 :
            self.error(self.logger.parameter_not_specified("command"))
            self.parser.exit_execution = True
            return

        self.command = self.command[1:]

    def run(self):
        global p
        p = subprocess.Popen(self.command, stdin=self.stdin, stdout=self.stdout, stderr=self.stderr, text=True)
        p.wait()
    
    def close(self):
        self.status = p.returncode if p else STATUS_ERR

