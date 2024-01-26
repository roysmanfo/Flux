from flux.core.helpers.arguments import Parser
from flux.core.helpers.commands import *
import os

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog="clear", description="clears the screen")
    
    def run(self):
        if os.name == 'nt':
            self.status = os.system("cls")
        else:
            self.status = os.system("clear")
        

