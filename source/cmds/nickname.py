from colorama import Fore
def run(cmd, courent_name):
    #Controllo che il comando sia corretto
    if len(cmd) == 1:
        print(f'{Fore.RED}Non hai inserito il nickname{Fore.WHITE}')
        return courent_name
    elif len(cmd) > 2:
        print(f'{Fore.RED}Hai inserito troppi argomenti{Fore.WHITE}')
        return courent_name
    
    #nickname --help
    if cmd[1].upper() == '--HELP' or cmd[1].upper() == '--H':
        help()
        return courent_name
    
    #Errore nella sintassi di --help
    elif cmd[1].upper() == '-HELP' or cmd[1].upper() == '-H':
        print(f'{Fore.WHITE}Forse volevi dire {Fore.CYAN}nickname --help{Fore.WHITE} oppure {Fore.CYAN}nickname --h{Fore.WHITE}?')
        return courent_name
    
    #Attributo inesistente
    elif '--' in cmd[1]:
        attr = cmd[1]
        print(f'{Fore.RED}Nessun attributo "{attr.upper()}" disponibile per il comando "nickname"{Fore.WHITE}')
        return courent_name
    
    #Cambio nickname
    else:
        return change(cmd)

def change(cmd):
    return cmd[1]

def help():
    print(f'{Fore.MAGENTA}Nickname')
    print(f'\n{Fore.WHITE}Serve a cambiare il nickname dell\'utente')
    print(f'{Fore.WHITE}Sintassi: nickname <nickname>')
    