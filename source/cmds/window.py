# Questo file si occupa di alcuni comandi che gestiscono un po' con l'applicazione

# TODO:
#   Assicurarsi che l'input sia corretto
#   Usare la libreria asyncio

#from asyncio import create_task, tasks
import os, asyncio, colorama
from colorama import Fore, Style

colorama.init()

def run(cmd:list) -> bool:#NOTE: questo comanso di default è solo per il testing
    import os, asyncio, colorama
    from colorama import Fore, Style
    colorama.init()


    if len(cmd) > 1:
        if cmd[1] == '--HELP' or cmd[1] == '--H':
            return Help.run(cmd)
        elif cmd[0] == 'CLOSE':
            return Close.start(cmd)
    else:

        if cmd[0] == 'CLOSE':
            return Close.close()
        elif cmd[0] == 'CLS':
            ClearScreen.clear()

class Close:
    # Sintassi: close | close <secondi> | close <opzione> <HH:MM:SS>
    def start(cmd: list, options: str = None) -> bool:
        if len(cmd) == 1:
            # close
            return Close.close()
        
        elif '-' in cmd[1][0] and '-' in cmd[1][1]:
            # Ha un attributo
            if cmd[1] == '--COUNTDOWN':
                try:
                    Close.close_with_countdown(int(cmd[2]) if len(cmd) > 2 else 10)
                except ValueError:
                    print(f'{Fore.RED}Errore: Il valore inserito non è un numero')
            else:
                print(f'{Fore.RED}Errore: l\'attributo "{Style.BRIGHT + cmd[1] + Style.NORMAL}" non è valido')
        #else:
            #Controlla se ha un orario
            #NOTE: il formato orario è HH:MM:SS

            #if ':' in cmd[1]:
            #    Close.programmed(cmd[1])
        else:
            print(f'{Fore.RED}Errore: l\'attributo "{Style.BRIGHT + cmd[1] + Style.NORMAL}" non è valido')  
            
        return
        #Close.programmed(cmd[1])
    
    def close() -> bool:
        print(f'{Fore.BLACK}',end='')
        os.system('exit')
        return False
        

    def close_with_countdown(n) -> bool:
        from .now import TimeUtils
        
        from colorama import Fore
        print(f'{Fore.RED}Il programma si chiuderà in ...')
        TimeUtils.countdown(n)
        return Close.close()

    def programmed(prefixed_time: str) -> None:
        from now import DateAndTime
        courent_time = DateAndTime.time()
        if courent_time == prefixed_time:
            os.system('start cmd')
        asyncio.sleep(1)
        print(courent_time)

    def help() -> None:
        print(f'{Fore.MAGENTA}CLOSE{Fore.WHITE}')
        print(f'\nPermette di chiudere l\'applicazione')
        print(f'\nSintassi: close <OPZIONE> | close <OPZIONE> <SECONDI>')
        print(f'OPZIONI:')
        print(f'\t--COUNTDOWN\t\tPermette di chiudere l\'applicazione mostrando un countdown in un numero di secondi')
        print(f'\t--HELP\t\t\tMostra questo messaggio')

class ClearScreen:
    def __init__(self):
        pass
    
    def clear() -> None:
        os.system('cls')

    def help() -> None:
        print(f'{Fore.MAGENTA}CLS{Fore.WHITE}')
        print(f'\nCancella tutto quel che e\' sullo schermo')
        print(f'Sintassi: cls')
        
class Help:
    def run(cmd: list) -> True:
        if cmd[0] == 'CLOSE':
            Close.help()
        elif cmd[0] == 'CLS':
            ClearScreen.help()

        return True

