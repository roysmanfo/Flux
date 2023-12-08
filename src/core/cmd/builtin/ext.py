import subprocess
from ...helpers.commands import *
from ...helpers.arguments import Parser



p: subprocess.Popen = None
class Command(CommandInterface):
    
    def init(self):
        self.parser = Parser("ext", description="Allows to use commands from outside flux")
        self.parser.add_argument("command", nargs="*", help="the command to run")

    def run(self):
        global p
        p = subprocess.Popen(self.args.command, stdin=self.stdin, stdout=self.stdout, stderr=self.stderr, text=True)
        p.wait()
    
    def close(self):
        self.status = p.returncode

