import colorama
from colorama import Fore
import random
from .helpers.commands import CommandInterface
from .helpers.arguments import Parser
colorama.init(autoreset=True)


class Command(CommandInterface):

    def init(self):
        self.parser = Parser("flux")


    def run(self, command: list[str]):
        self.args = self.parser.parse_args(command[1:])


        if len(command) == 1 or self.args.help:
            self.description(random.choice([0, 1]))


    def description(self, flip: bool = False):
        emotes = ["(╯°□°)╯︵ ┻━┻", "(ノಠ益ಠ)ノ彡┻━┻", "┬─┬ノ( º _ ºノ)", "¯\_(ツ)_/¯"]
        emote = random.choice(emotes) if flip else ""
        title = Fore.LIGHTBLACK_EX + """
    {:^27}
     _____ __    __ __  __  __ 
    |   __|  |  |  |  |\  \/  /
    |   _]|  |__|  |  | |    | 
    |__|  |_____\_____//__/\__\ 
            
    {:^27}
    
    """.format(emote, "By @RoysManfo")
        self.stdout.write(title + Fore.RESET + "\n")
