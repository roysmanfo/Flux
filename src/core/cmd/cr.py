def run(USER, LANG_FILE):
    with open(LANG_FILE, 'r') as lang_file:
        OUT = lang_file.readlines()


    print(
       f"""
                                            {OUT[0]}
  __________       _________         ____        ___________      _______________       ___________       _____
 /________/ |     /________/\       /___ /     /__________ /|    /_____________ /|     /_________ /|     /___ /|
|         | |    |         \ \     |    | |    |          | |    |             | |    |          | |    |    | |
|     ____|/     |          | |    |    | |    |    ______|/|    |____     ____|/     |     _    | |    |    | |
|    | |____     |         / /     |    | |    |          | |         |    |          |    |_|   | |    |    | |_____
|    |/___ /|    |         \ \     |    | |    |______    | |         |    |          |          | |    |    |/____ /|
|         | |    |    |\    \ \    |    | |    |          | |         |    |          |     |    | |    |          | |
|_________|/     |____|/\____\/    |____|/     |__________|/          |____|          |_____|____|/     |__________|/
       """ 
    )