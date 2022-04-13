#Dato un path di un file, restituisce il numero di file con estensione specificata.

import os
from colorama import Fore

def main(cmd):
    if cmd[1] == '--HELP' or cmd[1] == '-H':
        help()
    else:
        execute(cmd)

def count_extension(extension, pathToFile=None):
    try:
        
        if pathToFile is None or pathToFile == "":
            pathToFile = os.getcwd()
        count = 0
        for file in os.listdir(pathToFile):
            if file.endswith(extension):
                count += 1
        print(f'{Fore.WHITE}Sono presenti {count} file {extension} nella cartella: {pathToFile}')
    
    except OSError:
        #Se il path specificato non esiste verrà restituito un errore 
        print(f'{Fore.RED}Il percorso specificato non esiste')
        restart = input(f'{Fore.WHITE}Vuoi ripetere l\'operazione? (y/n):  {Fore.BLUE}')
        
        if restart == 'y':
            newPathToFile = input(f'{Fore.WHITE}Inserisci il nuovo percorso:  {Fore.BLUE}')
            count_extension(extension, newPathToFile)
        else:
            print(f'{Fore.RED}Operazione annullata{Fore.WHITE}')

def execute(cmd):
    extension = cmd[1].lower()
    try:
        pathToFile = cmd[2]
    except IndexError:
        pathToFile = None
    if pathToFile == '':
        pathToFile = None
    count_extension(extension, pathToFile)

def help():
    print(f'\n{Fore.WHITE}Questo comando permette di contare il numero di file con una determinata estensione')
    print(f'{Fore.WHITE}Sintassi: countfile <estensione> <percorso>')
    print(f'{Fore.WHITE}Se non viene specificato il percorso, verrà utilizzato il percorso corrente')
    print(f'\n{Fore.WHITE}Esempio: countfile.py .py')
    print(f'{Fore.WHITE}Esempio: countfile.py .py C:\\Users\\User\\Desktop\\test')