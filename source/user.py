"""
## File di gestione utenti

### Opzioni disponibili:
    - Flags: 
        - /logout
        - /new
    - Attrb:
        - --list
        - --help
"""

def run(cmd:list, user_name:str, user_id:str) -> None:
    
    if len(cmd) == 1:
        user_info(user_name, user_id)
    elif '--HELP' in cmd or '--H' in cmd:
        help()
    elif '--LIST' in cmd:
        user_list()
    elif '/LOGOUT' in cmd:
        user_logout(user_id)
        

def user_info(user_name:str, user_id:str) -> None:
    import json
    from json.decoder import JSONDecodeError
    from colorama import init, Fore
    init(autoreset=True)
    with(open(r'.\\users\\Users.json','r')) as l:
        try:
            f = json.load(l)
        except JSONDecodeError:
            f = {}
            print(f'{Fore.RED}Non ci sono utenti registrati')
            return
        role = f[str(user_id)]['role']
    
    print(f'{Fore.WHITE}\nID:\t\t{Fore.CYAN}{user_id}{Fore.WHITE}')
    print(f'{Fore.WHITE}Nome:\t\t{Fore.CYAN}{user_name}{Fore.WHITE}')
    print(f'{Fore.WHITE}Ruolo:\t\t{Fore.CYAN}{role}{Fore.WHITE}\n')

def user_list() -> None:

    import json
    from json.decoder import JSONDecodeError
    from colorama import init, Fore
    init(autoreset=True)
    with(open(r'.\\users\\Users.json','r')) as l:
        try:
            f = json.load(l)
        except JSONDecodeError:
            f = {}
            print(f'{Fore.RED}Non ci sono utenti registrati')
            return
        for key in f:
            print(f'{Fore.WHITE}\nID:\t\t{Fore.CYAN}{key}{Fore.WHITE}')
            print(f'{Fore.WHITE}Nome:\t\t{Fore.CYAN}{f[key]["name"]}{Fore.WHITE}')
            print(f'{Fore.WHITE}Ruolo:\t\t{Fore.CYAN}{f[key]["role"]}{Fore.WHITE}\n')

def user_logout(user_id) -> None:
    import json, time, Login
    from colorama import init, Fore
    init(autoreset=True)

    with open(r'.\\users\\Users.json','r') as l:
        f = json.load(l)
        f[str(user_id)]['status'] = 'Inactive'
    with open(r'.\\users\\Users.json','w') as l:
        json.dump(f, l, indent=4)
    print(f'{Fore.GREEN}Logout effettuato con successo')
    time.sleep(2)
    Login.log(None)

def help() -> None:
    from colorama import init, Fore
    init(autoreset=True)

    print(f'{Fore.MAGENTA}USER\n{Fore.RESET}')
    print(f'Serve a gestire gli utenti')
    print(f'{Fore.WHITE}SINTASSI: user | user [OPZIONE]\n{Fore.RESET}')
    print(f'{Fore.WHITE}OPZIONI:{Fore.RESET}')
    print(f'{Fore.WHITE}\t\LOGOUT:\tEffettua il logout dall\'utente in uso{Fore.RESET}')
    print(f'{Fore.WHITE}\t\\NEW:\t\tPermette di creare un nuovo utente (max 10){Fore.RESET}\n')
    print(f'{Fore.WHITE}\t--LIST:\t\tStampa tutti gli utenti registrati{Fore.RESET}')
    print(f'{Fore.WHITE}\t--HELP:\t\tStampa questo messaggio{Fore.RESET}')
#Permette di creare un nuovo utente (max 10)