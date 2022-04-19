#NOTE: il comando nickname è un comando che non funziona, perchè non cambia il nick
import os, json
import colorama
from colorama import Fore
import Login, cmdhandler, utils

colorama.init(autoreset=True)

ReadyToStart = False
dir = os.getcwd()+"\\Cristal"
# "BIOS" - Serve a controllare che sia tutto a posto prima di avviare il programma
isLogged, user, nick = Login.log(dir)

while ReadyToStart == False:
    if isLogged == 0:
        ReadyToStart = True
        break
    if isLogged == 1:   
        isLogged, user, nick = Login.log(dir)
    if isLogged == 2:
        isLogged =  Login.reLog()

user = f'User{user}'
NAME = nick
#Inizio
continue_execution = True
while continue_execution:
    #Input dell'utente
    cmd = input(f'{Fore.WHITE}{str(nick)}{Fore.BLUE}>  ')
    #Transformo il comando in una lista
    cmd = utils.Utils.string_to_list(cmd)

    #In questo modo anche se l'utente mescola lettere maiuscole e minuscole,
    #il comando sarà sempre in maiuscolo
    cmd[0] = cmd[0].upper()
    with open(f'{os.getcwd()}\cmds\\files\\commands_{NAME}.json','r') as file:
        cmdNames = json.load(file)
        if cmd[0] == cmdNames['NICKNAME']:
            import cmds.nickname
            nick = cmds.nickname.run(cmd, nick)
        if cmd[0] == cmdNames['CLOSE']:
            import cmds.window
            cmd = [ i.upper() for i in cmd ]
            continue_execution = cmds.window.run(cmd)
        else:
            cmd = [ i.upper() for i in cmd ]
            cmdhandler.cmd(cmd, NAME)
