#Dato un path di un file, restituisce il numero di file con estensione specificata.
#esempio:
#input: .py
#percorso: C:\Users\User\Desktop\python\test
#output: Sono presenti 81989 file .dll nella cartella: C:\Users\User\Desktop\python\test
#se non viene fornito il path, viene utilizzato il percorso corrente

def count_extension(extension, pathToFile=None):
    try:
        import os
        from colorama import Fore
        if pathToFile is None or pathToFile == "":
            pathToFile = os.getcwd()
        count = 0
        for file in os.listdir(pathToFile):
            if file.endswith(extension):
                count += 1
        print(f'{Fore.WHITE}Sono presenti {count} file {extension} nella cartella: {pathToFile}')
    except Exception:
        #Se il path specificato non esiste verrà restituito un errore
        print(f'{Fore.Red}Sono presenti {count} file {extension} nella cartella: {pathToFile + Fore.WHITE}')
        path = None
        count_extension(extension, path)