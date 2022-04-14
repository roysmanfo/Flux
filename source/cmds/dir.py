import os
from colorama import Fore

def run(cmd):
    if  cmd == ['DIR']:
        i=0
        for cartella, sottocartelle, file in os.walk(os.getcwd()):
            i+=1
            if i == 1:
                print(f"{Fore.WHITE}Ci troviamo nella cartella: '{cartella}'")
            elif i == 2:
                print(f"{Fore.WHITE}Le sottocartelle presenti sono: '{sottocartelle}'")
    else:
        if cmd[1] == '--HELP' or cmd[1] == '--H':
            help()

        elif len(cmd)<=3 and '--ITEMS' in cmd and '--DIR' in cmd:
            Execution.legth()
            Execution.items()
        elif cmd[1] == '--ITEMS':
            Execution.items()
        elif cmd[1] == '--LEGHT':
            Execution.legth()
        else:
            print(f'{Fore.RED}Comando non riconosciuto{Fore.RESET}')

class Execution:
    def items():
        for i in os.listdir():
            print(i)
    def legth():
        num = 0
        for i in os.listdir():
            num +=1
        print(f'{Fore.WHITE}Sono presenti {num} elementi tra file e cartelle')

def help():
    print(f'{Fore.MAGENTA}DIR{Fore.RESET}')
    print('\nQuesto comando permette di visualizzare i file e le cartelle presenti nella directory corrente')
    print('Sintassi: dir [OPZIONI]')
    print('\nOPZIONI:')
    print('\t--ITEMS\t\tVisualizza i file e le cartelle presenti nella directory corrente')
    print('\t--LEGHT\t\tVisualizza il numero di elementi presenti nella directory corrente')
    print('\t--HELP\t\tVisualizza questo messaggio')
