import random
from flux.core.helpers.commands import CommandInterface
from flux.core.helpers.arguments import Parser

class Command(CommandInterface):

    def init(self):
        self.parser = Parser("flux")

    def setup(self):
        if "-h" in self.command or "--help" in self.command:
            self.banner(random.choice([0, 1]))
        super().setup()


    def run(self):
        if self.parser.no_args:
            self.print(self.banner)

    @property
    def banner(self):
        emotes = [r"(╯°□°)╯︵ ┻━┻", r"(ノಠ益ಠ)ノ彡┻━┻", r"┬─┬ノ( º _ ºノ)", r"¯\_(ツ)_/¯"]
        emote = random.choice(emotes) if random.choice([0, 1]) else ""
        banner = self.colors.Fore.LIGHTBLACK_EX + r"""
        {:^27}
         _____ __    __ __  __  __ 
        |   __|  |  |  |  |\  \/  /
        |   _]|  |__|  |  | |    | 
        |__|  |_____\_____//__/\__\ 
                
        {:^27}
        
        """.format(emote, "By @roysmanfo")
        return banner + self.colors.Fore.RESET


