import json
from colorama import Fore
class General:
    def help() -> None:
        import os
        cDir = f'{os.getcwd()}\\cmds\\files\\'
        with open(f'{cDir}\\commands.json','r') as file:
            l = json.load(file)
            print(f'{Fore.CYAN}\nComandi disponibili:\n')
            for i in l:
                print(f'{Fore.WHITE + l[i].upper()}')
            print('\nPer ulteriori informazioni su uno specifico comando, digitare "nome_comando --help"')
    
    def help_detailed() -> None:
        #Qui verranno date informazioni sulla sintassi dei comandi
        pass

class Hidden:
    # comandi nascosti
    pass