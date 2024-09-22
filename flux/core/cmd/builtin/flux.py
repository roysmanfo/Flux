import random
from flux.core.helpers.commands import (
    CommandInterface,
    Parser
)

EMOTES = [
    r"(ง ͠° ͟ل͜ ͡°)ง",
    r"(╯°□°)╯︵ ┻━┻",
    r"(ノಠ益ಠ)ノ彡┻━┻",
    r"┬─┬ノ( º _ ºノ)",
    r"¯\_(ツ)_/¯",
    r"( ͡◉ ͜ʖ ͡◉)",
    r"(  ಠ_ಠ )",
    r"(ꐦ ಠ皿ಠ )",
    r" ̿̿ ̿̿ ̿̿ ̿'̿'\̵͇̿̿\з=(◣_◢)=ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿ ",
    r"ᕦ(⌐■ ͜ʖ■)ᕥ",
    r"\_(ಠ_ಠ)_/",
    r"┻━┻ ¯\_(ಠ□ಠ)_/¯ ┻━┻",
    r"(ノಠ益ಠ)ノ彡┻━┻ ლ(ಠ益ಠლ)",
]

class Command(CommandInterface):

    def init(self):
        self.parser = Parser("flux")

    def setup(self) -> None:

        if any(map(lambda x: x in self.line_args, ("-h", "--help"))):
            self.print(self.banner())
        super().setup()

    def run(self):

        if len(self.line_args) == 1:
            self.print(self.banner())


    def banner(self):
        emote = random.choice(EMOTES)
        banner_width = 38
        pad_len = max(0, (banner_width - len(emote)) // 2)
        pad = " " * pad_len
        emote = pad + emote
        title = fr"""
        {emote}
         ____       _____ __    __ __  __  __ 
        |    |___  |   __|  |  |  |  |\  \/  /
        |___|    | |   _]|  |__|  |  | |    | 
            |____| |__|  |_____\_____//__/\__\ 
                
        {'By @roysmanfo':^38}
        
        """
        return self.colors.Fore.LIGHTBLACK_EX + title + self.colors.Fore.RESET


