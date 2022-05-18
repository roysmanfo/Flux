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
    elif '--list' in cmd:
        user_list()

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