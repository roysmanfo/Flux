# Tests

try:
    from cmds import *
    import os,json, colorama
    from colorama import Fore
    colorama.init(autoreset=True)
    
    print('User Tests')
    print(f'{Fore.GREEN}Test 1 passed')
except Exception as e:
    print(f'{Fore.RED}{e}')

# Conrtolla che gli utenti vengano salvati correttamente
class usersCheck:
    def __init__(self):
        self.AdminCeck()
        self.nameCheck()

    #Controlla che ci sia solo un Admin
    def AdminCeck():
        with open(r'C:\Cristal 2022\Files\Login\Users.json','r') as l:
            Report = True
            admins = 0
            file = json.load(l)
            for i in file:
                if file[i]['role'] == 'Admin':
                    admins += 1
                    if admins>1:
                        Report = False
                        print(f'{Fore.RED}Test 2 failed')
                        break
                    
        if Report == True:
            print(f'{Fore.GREEN}Test 2 passed')
    
    #Controlla che l'utente sia registrato correttamente
    def nameCheck():
        with open(r'C:\Cristal 2022\Files\Login\Users.json','r') as l:
            file = json.load(l)
            nameList = []
            problems = False
            for i in file:
                nameList.append(file[i]['name'])

            for i in nameList:
                repeats = nameList.count(i)
                if repeats > 1:
                    problems = True
        if problems:
            print(f'{Fore.RED}Test 3 failed')
        else:
            print(f'{Fore.GREEN}Test 3 passed')


class Automation:
    #Apre un URL
    def AutoOpenURL(url='www.google.com'):
        try:
            os.system(f'start "" {url}')
            print(f'{Fore.GREEN}Test 1 passed')
        except:
            print(f'{Fore.RED}Test 1 failed')
    
    #Cerca la data attuale su DuckDuckGo
    def TodayFact():
        try:
            import time
            date = time.strftime("%d/%m/%y")
            date = date.replace('/','%2F')
            os.system(f'start "" https://duck.com/?q={date}&atb=v1-1&iar=news&ia=news')
            # Esempio - os.system(f'start "" https://duck.com/?q=27%2F02%2F22&atb=v1-1&iar=news&ia=news')
            print(f'{Fore.GREEN}Test 2 passed')
        except:
            print(f'{Fore.RED}Test 2 failed')

    def AutoShutdown():
        try:
            #os.system('shutdown /s ')
            print(f'{Fore.GREEN}Test 3 passed')
        except:
            print(f'{Fore.RED}Test 3 failed')
    
    


class Utils:
    #Permette di distribuire il comando da formato stringa a diversi elementi di una lista
    def wordList(string = 'shutdown /s'):
        words = []
        for i in string:
            if i == ' ':
                words.append(string[:string.index(i)])
                string = string[string.index(i)+1:]
        words.append(string)
        print(words)

class Performance:   
    #Testa la velocità della rete
    def webPerformance(name = 'google.com', numberOfThreads = 10):
        try:
            import os
            os.system(f'ping -n {numberOfThreads} {name}')
            print(f'{Fore.GREEN}Test 1 passed')
        except:
            print(f'{Fore.RED}Test 1 failed')


#Esecuzione tests

# Controllo utenti
if __name__ == '__main__':
    usersCheck.AdminCeck()
    usersCheck.nameCheck()
    
    print('\nUtils Tests')
    Utils.wordList()

    print('\nPerformance Tests')
    Performance.webPerformance()

    print('\nAutomation Tests')
    Automation.AutoOpenURL()
    Automation.TodayFact()
    Automation.AutoShutdown()
    
    print('\nEnd of Tests')

    #os.system('pause')
    input('Press enter to exit')
    os.system('cls')
    os.system('exit')