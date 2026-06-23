import time
from flux.core.interfaces import CommandInterface
from flux.core.interfaces.commands import Parser



class Command(CommandInterface):

    def init(self):
        self.parser = Parser("time", description="get time in seconds")
        self.parser.add_argument("command", nargs="*", help="the command whose performance is to be measured")

    def run(self):
        start = time.time()
        if self.args.command:
            self.system.run(self.args.command)        
        self.print(f"{(time.time()-start)}s")
