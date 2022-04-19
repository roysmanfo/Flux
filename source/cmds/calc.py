# Calc - Calculator
# Calcola il valore di addizioni, sottrazioni, moltiplicazioni,
# divisioni e risolve anche espressioni numeriche
from colorama import Fore

def run(cmd):
    if len(cmd) == 1:
        calc()
    
    elif cmd[1] == '--HELP' or cmd[1] == '--H':
        help()
    elif cmd[1] == '-HELP' or cmd[1] == '-H':
        print(f'{Fore.WHITE}Forse volevi dire {Fore.CYAN}calc --help{Fore.WHITE} oppure {Fore.CYAN}calc --h{Fore.WHITE}?')
    else:
        if cmd[1][0] == '-' and cmd[1][1] == '-':
            print(f'{Fore.WHITE}L\'attributo "{Fore.YELLOW}{cmd[1]}{Fore.WHITE}" non esiste')

def calc():
    try:
        operation = input(f'{Fore.WHITE}Inserire l\'operazione:  {Fore.RESET}')
        print(f'{str(operation)} = {str(eval(operation))}')
    except Exception:
        print(f'{Fore.RED}Errore: Inserire un\'operazione valida{Fore.RESET}')

def help():
    print(f'{Fore.MAGENTA}Calc - Calculator')
    print('\nCalcola il valore di addizioni, sottrazioni, moltiplicazioni, divisioni e risolve anche espressioni numeriche')
