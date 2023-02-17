import colorama
from colorama import Fore

colorama.init(autoreset=True)

def run(USER):
    pass

def description(USER):
    title = f"""{Fore.LIGHTBLACK_EX}
   __________       _________         _____       ___________      _______________       ___________       _____        
  /_________/|     /________/\       /___ /|    /__________ /|    /_____________ /|     /_________ /|     /___ /|       
 |         | |    |         \ \     |    | |    |          | |    |             | |    |          | |    |    | |       
 |     ____|/     |          | |    |    | |    |    ______|/|    |____     ____|/     |     _    | |    |    | |       
 |    | |____     |         / /     |    | |    |          | |         |    |          |    |_|   | |    |    | |_____  
 |    |/___ /|    |         \ \     |    | |    |______    | |         |    |          |          | |    |    |/____ /| 
 |         | |    |    |\    \ \    |    | |    |          | |         |    |          |     |    | |    |          | | 
 |_________|/     |____|/\____\/    |____|/     |__________|/          |____|          |_____|____|/     |__________|/  
{Fore.RESET}
"""
    print(title)


def get_variables(INFO: object, variable: str) -> None:
    import os
    from dotenv import load_dotenv

    load_dotenv(verbose=False)
    RESERVED_VARS = os.getenv('RESERVED_VARS').split(", ")
    variable = variable.removeprefix('$')

    if variable not in RESERVED_VARS:
        var = INFO.variables.get(variable, None)
        if var is None:
            print(f"No variable ${variable} found")
            return
        print(f'${variable}={var}')
    else:
        if variable == RESERVED_VARS[0]:
            if INFO.variables:
                for v in INFO.variables.keys():
                    print(f'${v} = {INFO.variables.get(v)}')

            else:
                print('No variables created yet')