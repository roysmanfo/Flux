# Funzioni untili per il progetto

class Utils:
    #scrivi una funzione che data una stringa, restituisce una lista di parole
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

class Performance:   
    #Testa la velocità della rete
    def webPerformance(name = 'roysmanfohub.web.app', numberOfThreads = 10):
        try:
            import os
            os.system(f'ping -n {numberOfThreads} {name}')
            #print(f'{Fore.GREEN}Test 1 passed')
        except:
            #print(f'{Fore.RED}Test 1 failed')
            return False

class Security:
    def cript(string:str=None):
        if string == None:
            return None
        else:
            return string.encode('utf-8').hex()
    def decript(string:str=None):
        if string == None:
            return None
        else:
            return bytes.fromhex(string).decode('utf-8')
