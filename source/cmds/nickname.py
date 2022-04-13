from colorama import Fore
def run(cmd, courent_name):
    if cmd[1].upper() == '--HELP' or cmd[1].upper() == '--H':
        help()
        return courent_name
    elif cmd[1].upper() == '-HELP' or cmd[1].upper() == '-H':
        print(f'{Fore.WHITE}Forse volevi dire {Fore.CYAN}nickname --help{Fore.WHITE}?')
        return courent_name
    else:
        return change(cmd)

def change(cmd):
    return cmd[1]

def help():
    print(f'\n{Fore.WHITE}Sintassi: nickname <nickname>')
    print(f'{Fore.WHITE}Serve a cambiare il nickname dell\'utente')