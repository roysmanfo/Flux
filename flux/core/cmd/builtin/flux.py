import random
from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)

class Command(CommandInterface):

    def init(self):
        self.parser = Parser("flux")


    def run(self):

        if len(self.command) == 1 or self.args.help:
            self.description(random.choice([0, 1]))


    def description(self, flip: bool = False):
        emotes = [r"(╯°□°)╯︵ ┻━┻", r"(ノಠ益ಠ)ノ彡┻━┻", r"┬─┬ノ( º _ ºノ)", r"¯\_(ツ)_/¯"]
        emote = random.choice(emotes) if flip else ""
        title = self.colors.Fore.LIGHTBLACK_EX + r"""
        {:^27}
         _____ __    __ __  __  __ 
        |   __|  |  |  |  |\  \/  /
        |   _]|  |__|  |  | |    | 
        |__|  |_____\_____//__/\__\ 
                
        {:^27}
        
        """.format(emote, "By @roysmanfo")
        self.print(title + self.colors.Fore.RESET)


