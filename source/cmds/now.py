from colorama import Fore

def run(cmd):
    if len(cmd) > 1:
        if cmd[1] == '--HELP' or cmd[1] == '--H':
            if cmd[0] == 'DATE':
                Help.date_help()
            elif cmd[0] == 'TIME':
                Help.time_help()
        elif cmd[1] == '--HELP-ALL' or cmd[1] == '--HA':
            Help.date_help()
            Help.time_help()
        else:
            print(Fore.RED + 'Error: Invalid command.')
    else:
        if cmd[0] == 'DATE':
            DateAndTime.date()
        elif cmd[0] == 'TIME':
            DateAndTime.time()
        else:
            print(Fore.RED + 'Error: Invalid command.')
        
class DateAndTime():
    def date():
        #Scrive la data attuale
        import datetime
        now = datetime.datetime.now()
        print(now.strftime("%d/%m/%Y"))

    def time():
        #Scrive l'ora attuale
        import datetime
        now = datetime.datetime.now()
        print(now.strftime("%H:%M:%S"))

class Help():
    def date_help():
        #Scrive l'help per la data
        print(f'\n{Fore.MAGENTA}Date{Fore.WHITE}')
        print('Scrive la data attuale')
        print('Sintassi: date | date [OPZIONE]')
        print('OPZIONI:')
        print('\t--HELP | --H:\t\tScrive l\'help per la data')
        print('\t--HELP-ALL | --HA:\tScrive l\'help per la data e l\'ora')
        
    def time_help():
        #Scrive l'help per l'ora
        print(f'\n{Fore.MAGENTA}Time')
        print(f'{Fore.WHITE}Scrive l\'ora attuale')
        print(f'{Fore.WHITE}Sintassi: time | time [OPZIONE]')
        print(f'{Fore.WHITE}OPZIONI:')
        print(f'{Fore.WHITE}\t--HELP | --H:\t\tScrive l\'help per l\'ora')
        print(f'{Fore.WHITE}\t--HELP-ALL | --HA:\tScrive l\'help per la data e l\'ora')
