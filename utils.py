# Funzioni untili per il progetto

class Utils:
    #Permette di distribuire il comando da formato stringa a diversi elementi di una lista
    def decode(string = 'shutdown /s'):
        words = []
        for i in string:
            if i == ' ':
                words.append(string[:string.index(i)])
                string = string[string.index(i)+1:]
        words.append(string)
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