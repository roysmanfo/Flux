#Dato un path di un file, restituisce il numero di file con estensione specificata.
#esempio:
#input: .py
#percorso: C:\Users\User\Desktop\python\test
#output: Sono presenti 81989 file .py nella cartella: C:\Users\User\Desktop\python\test
#se non viene fornito il path, viene utilizzato il percorso corrente
import os
from colorama import Fore

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

def execute():
    extension = input(f'{Fore.WHITE}Inserisci l\'estensione: {Fore.BLUE}')
    pathToFile = input(f'{Fore.WHITE}Inserisci il percorso del file: {Fore.BLUE}')
    if pathToFile == '':
        pathToFile = None
    count_extension(extension, pathToFile)