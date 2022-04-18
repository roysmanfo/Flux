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
            DateAndTime.response(cmd[0])
        elif cmd[0] == 'TIME':
            DateAndTime.response(cmd[0])
        else:
            print(Fore.RED + 'Error: Invalid command.')
        
class DateAndTime():
    def response(command):
        if command == 'DATE':
            print(DateAndTime.date())
        elif command == 'TIME':
            print(DateAndTime.time())
        
    def date() -> str:
        #Restituisce la data attuale
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%d/%m/%Y")

    def time() -> str:
        #Restituisce l'ora attuale
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S")

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

class TimeUtils:
    def countdown(n:int) -> None:
        import time
        start = n + 1 #In questo modo stampa anche 0
        for _ in range(start):
            print(n)
            n -= 1
            time.sleep(1)
