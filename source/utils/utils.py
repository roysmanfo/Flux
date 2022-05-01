# Funzioni untili per il progetto

class Utils:
    #Data una stringa, restituisce una lista di parole
    def string_to_list(string:str=None):
        if string == None or string == '':
            string = ['']
            return string
        else:
            return Utils.decode(string)

    #Permette di distribuire il comando da formato stringa a diversi elementi di una lista
    def decode(string:str=None):
        words = []
        for i in string:
            if i == ' ':
                words.append(string[:string.index(i)])
                string = string[string.index(i)+1:]
        words.append(string)
        leght = len(words)
        while leght > 0:
            if words[leght-1] == '':
                words.pop(leght-1)
            leght -= 1
        return words
    
    #Esegue un contdown da un determinato numero
    def countdown(n:int) -> None:
        import time
        for _ in range(n):
            print(n)
            n -= 1
            time.sleep(1)
    
    #Restituisce il path della directory specificata
    def get_path_dir(target_dir:str) -> str:
        import os
        return os.path.join(os.path.expanduser('~'), target_dir)
    
    #Restituisce il path del file specificato
    def get_path_file(target_dir:str, file_name:str) -> str:
        import os
        return os.path.join(os.path.expanduser('~'), target_dir, file_name)
    
    #Controlla se una directory esiste
    def check_if_dir_exists(target_dir:str) -> bool:
        import os
        return os.path.isdir(target_dir)
    
    #Controlla se un file esiste
    def check_if_file_exists(target_dir:str, file_name:str) -> bool:
        import os
        return os.path.isfile(target_dir, file_name)

class Performance:   
    #Testa la velocità della rete
    def ping(name:str = 'roysmanfohub.web.app', numberOfThreads:int = 10) -> None:
        try:
            import os
            os.system(f'ping -n {numberOfThreads} {name}')
            #print(f'{Fore.GREEN}Test 1 passed')
        except:
            #print(f'{Fore.RED}Test 1 failed')
            return False

class Security:
    
    #Permette di cifrare la password
    def cript(string:str=None) -> str:
        if string is None:
            return None
        else:
            return string.encode('utf-8').hex()
    
    #Permette di decifrare la password
    def decript(string:str=None) -> str:
        if string is None:
            return None
        else:
            return bytes.fromhex(string).decode('utf-8')
