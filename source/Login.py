# Cristal 2022
# Sequenza di login/register

import json, colorama
from json.decoder import JSONDecodeError
import os, time
from colorama import Fore, Style
import utils
colorama.init(autoreset=True)

userRole = ''
tree = '\\Cristal\\Files\\Login'
n = 0
def roleCheck():#Serve a sapere che ruolo dare all'utente se non c'è un admin
    global userRole
    i = open(f'{tree}\\Users.json','w')
    i.close()
    with open(f'{tree}\\Users.json','r') as l:
        try:
            f = json.load(l)
            becomeAdmin = False
        except JSONDecodeError:
            becomeAdmin = True
        if becomeAdmin:
            userRole = 'Admin'
        else:
            userRole = 'Guest'
    return userRole
def numberCheck() -> int:
    global n
    with open(f'{tree}\\Users.json','r') as l:
        try:
            f = json.load(l)
            n = 0
            n = len(f)
        except JSONDecodeError:
            n = 1
    return n + 1
def register(dir):
            role = str(roleCheck())
            userNumber = numberCheck()

            UserNameApproved = False
            while UserNameApproved != True:
                            UserName = input('Nome utente:  ')
                            with open(f'{tree}\\Users.json','r') as l:
                                try:
                                    file = json.load(l)
                                    for i in file:
                                        name = file[i]['name']
                                        if UserName != name:
                                            UserNameApproved = True
                                    print(f'\nA quanto pare, esiste già un utente con {Style.BRIGHT}{UserName}{Style.RESET_ALL} come nome utente')
                                    print('Prova con un nuovo nome utente\n')
                                except JSONDecodeError:
                                    UserNameApproved = True
            UserPassword = ''
            while len(UserPassword) < 8:
                UserPassword = input('Password:  ')
                if len(UserPassword) < 8:
                    print(f'{Fore.RED}La password deve essere di almeno 8 caratteri{Fore.WHITE}')
            
            UserPassword = utils.Security.cript(UserPassword)

            Dir = os.getcwd()
            # Controllo o creazione della directory dove verrà salvato il file Users.json
            try:
                os.chdir(f'{tree}\\')
            except IOError or FileNotFoundError or OSError :
                os.makedirs(f'{tree}\\')
                os.chdir(f'{tree}\\')
            # Scrittura sul file
            with open('Users.json', 'w') as fileCredenziali:
                User = {
                    "name": f'"{UserName}",',
                    "password": f'"{UserPassword}",',
                    "email": 'null,',
                    "role": f'"{role}",',
                    "status": '"Online"'# Andrà cambiato in offline quando si scrive il comando close
                }

                fileCredenziali.writelines('{\n    "User'+str(userNumber)+'": {')
                for i in User:
                    fileCredenziali. writelines(f'\n        "{i}": {User[i]}')

                fileCredenziali.writelines("\n    }\n}\n")
            
            # Creazione del file settings.json

            with open(f'{tree}\\settings.json','w') as file:
                settings = {
                    "dir": {
                        "defoult-output-dir": '"\documents\Cristal\output",',
                    },
                    "lang": {
                        "file-lang": '"it",',
                    }
                }
                #Scrivi sul file settings.json i valori di default contenuti in settings usando json.dump
                json.dump(settings, file)

            os.chdir(dir)

            #Scrittura file contenente lista comandi personalizzabili
            commandFile = open(f'{dir}\\cmds\files\commands.json','r')
            with open(f'{dir}\\cmds\\files\\commands{UserName}.json','w') as file:
                file.writelines(commandFile)

            print(f'{Fore.GREEN}Registrazione completata con successo')
            os.chdir(Dir)
def log(dir):
    
    #Utente registrato nell'app
    try:
        #Controlla se ci sono le credenziali
        try:
            with open(f'{tree}\\Users.json','r') as f:
                i = os.getcwd()
                os.chdir(f'{tree}\\')
                os.chdir(i)
                l = json.load(f)
                #Controlla se ci sono più utenti, se si, chiede quale utente vuole loggare
                if len(l) > 1:
                    print('Quale utente si vuole utilizzare?')
                    c = 0
                    for j in l:
                        c += 1
                        print(j, str(l[f'User{str(c)}']['name']))
                    print()
                    user = input('User')
                else:
                    user = 1
                os.system('cls')#Pulisce la console
                username = l[f'User{str(user)}']['name']
                wellcome = f'Benvenuto in Cristal, { str(username) }'
                for i in wellcome:
                    print(i, end='')
                    time.sleep(0.025)
                print()
            
            return 0, user, str(l[f'User{user}']['name']) # Tutto apposto, il file è presente e l'utente è loggato
        except Exception:
            os.makedirs(f'{tree}\\')
            os.chdir(f'{tree}\\')
            print(f'{Fore.RED}\nC\'e stato un problema con il file, si è verificato un errore')
            return 2, None # Il file è presente, ma modificato o corrotto

    #Utente non registrato nell'app
    except FileExistsError:

        print('Pare che tu non sia registrato...')
        print('Crea un utente per poter usare Cristal\n')

        register(dir)
        return 1, None, None # Va riavviata la funzione
def reLog():
    Dir = os.getcwd()
    os.remove(f"{tree}/Users.json")
    os.chdir(Dir)
    print('Possibile soluzione al problema, si prega di rieffettuare il login')
    return 1, None
def logout(dir):
    # NOTE: Questa funzione non è ancora stata implementata

    Dir = os.getcwd()
    os.chdir(f'{tree}\\')
    os.remove(f'Users.json')
    os.chdir(Dir)
    return 1, None


if __name__ == '__main__':
    print('Questo file non è eseguibile')
    os.system('pause')