import colorama
from colorama import Fore
import random
from flux.core.helpers.commands import CommandInterface
from flux.core.helpers.arguments import Parser
colorama.init(autoreset=True)


class Command(CommandInterface):

    def init(self):
        self.parser = Parser("flux")


    def run(self):

        if len(self.command) == 1 or self.args.help:
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
        self.print(title + Fore.RESET)
