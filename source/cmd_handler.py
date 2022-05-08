# Cristal 2022
# Gestore dei comandi (cmdhandler)

# ____    ___   _ _   _____
# | | \  /   \ | | | / ___/
# | __/  | | |  \ /  \__ \
# | | \  \___/   |  /____/

import json
from colorama import Fore
from .utils import update

def cmdNotFound(problem):
    print(problem)

def cmd(cmd,username):
    update.update(cmd)
    Fore.RESET
    #Permette al cmdhandler di accedere al nome dei comandi
    import os
    cDir = os.getcwd()+'\\Cristal'

    #Controllo del comando inserito
    with open(f'{os.getcwd()}\\cmds\\files\\commands_{username}.json','r') as file:
        try:

            command = json.load(file)

            if cmd[0] == command['CALC']:
                from cmds import calc
                calc.run(cmd)
                return

            elif cmd[0] == command['COUNTFILE']:
                from cmds import countfile
                countfile.run(cmd)
                return

            elif cmd[0] == command['CLS']:
                from cmds import window
                window.run(cmd)
                return

            elif cmd[0] == command['DIR']:
                from cmds import dir
                dir.run(cmd)
                return

            elif cmd[0] == command['DATE']:
                from cmds import now
                now.run(cmd)
                return

            elif cmd[0] == command['HELP']:
                import cmds.help
                cmds.help.General.help()
                return
            
            elif cmd[0] == command['TIME']:
                from cmds import now
                now.run(cmd)
                return

            else:
                if cmd == ['']:
                    return
                else:
                    print(f'{Fore.WHITE}Il comando "{Fore.YELLOW + cmd[0] + Fore.WHITE}" è un comando sconosciuto')
      
        except Exception as problem:
            cmdNotFound(problem)
        