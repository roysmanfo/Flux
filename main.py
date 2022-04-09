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
username = nick
NAME = nick
#Inizio
for i in range(5):
    cmd = input(f'{Fore.WHITE + nick + Fore.BLUE}>  ')#Input dell'utente
    cmd = utils.Utils.decode(cmd)#Transformo il comando in una lista

    with open(f'{os.getcwd()}\\cmds\\files\\commands_{NAME}.json','r') as file:
        cmdNames = json.load(file)
        if cmd[0] == cmdNames['NICKNAME']:
            import cmds.nickname
            nick = cmds.nickname.change(username)
        else:
            cmdhandler.cmd(cmd, username)
