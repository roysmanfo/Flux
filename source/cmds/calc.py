# Calc - Calculator
# Calcola il valore di addizioni, sottrazioni, moltiplicazioni,
# divisioni e risolve anche espressioni numeriche
from colorama import Fore
def calc():
    operation = input(f'{Fore.WHITE}Inserire l\'operazione:  {Fore.RESET}')
    print(f'{str(operation)} = {str(eval(operation))}')