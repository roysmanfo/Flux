# GitHub: RoysManfo/Cristal
# Description: Main file for the program
#   ______    ___  ___ 
#  |      \  |   \/   |
#  |  | __/  |        |
#  |  |  \   |  |\/|  |
#  |__|\__\  |__|  |__|
#

import os, json
import colorama
from colorama import Fore
import Login, cmd_handler
from utils import utils

colorama.init(autoreset=True)

ReadyToStart = False
dir = os.getcwd()+"\\Cristal"
# "BIOS" - Serve a controllare che sia tutto a posto prima di avviare il programma
isLogged, user_id, nick = Login.log(dir)

while ReadyToStart == False:
    if isLogged == 0:
        ReadyToStart = True
        break
    if isLogged == 1:   
        isLogged, user_id, nick = Login.log(dir)
    if isLogged == 2:
        isLogged, user_id, nick =  Login.reLog()

NAME = nick
#Inizio
#os.chdir(utils.Utils.get_path_dir('Desktop'))
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

        elif cmd[0] == cmdNames['CLOSE']:
            import cmds.window
            cmd = [ i.upper() for i in cmd ]
            continue_execution = cmds.window.run(cmd)
        elif cmd[0] == cmdNames['USER']:
            import user
            cmd = [ i.upper() for i in cmd ]
            user.run(cmd, NAME, user_id)
        else:
            cmd = [ i.upper() for i in cmd ]
            cmd_handler.cmd(cmd, NAME)
