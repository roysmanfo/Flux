from gtts import gTTS
import speech_recognition as sr
import os

# NOTE: Questa funzione non è ancora stata implementata
# NOTE: Le informazioni verranno richieste in modo separato e non tutto in una riga

# Sintassi: speech --audio [OPZIONE]             Conversione file
#           speech --audio                       Conversione testo   

# Sintassi: speech --text [OPZIONE]              Conversione file
#           speech --text                        Conversione testo

def run(cmd:list, user_name:str, settings_file_path:str):
    import os, sys
    courent_dir = os.getcwd()
    sys.path.append(os.chdir('..\\'))
    import utils
    from colorama import Fore
    if cmd[1] == '--AUDIO' and '--TEXT' not in cmd:
        if '--FILE' in cmd:
            # .txt => .mp3
            
            lang = input('Lingua: ')
            name = input('Nome file: ')

            while go_on == False:
                filePath = input('Percorso file: ')
                if os.path.isfile(filePath):
                    go_on = True
                else:
                    print(f'{Fore.RED}Il file {filePath} non esiste{Fore.RESET}')
                    go_on = False

            text = open(filePath, 'r').read()
            fileDestination = input('Percorso destinazione: ')
            
            TextToSpeech.convert_to_speeck(text, lang, name, fileDestination, settings_file_path)

        elif '--FILE' not in cmd:
            # text => .mp3
            pass
            

class TextToSpeech:
    def convert_to_speeck(text:str, lang:str, name:str, file_path:str, destination:str, settings_file_path:str) -> None:
        import json, utils, colorama
        from colorama import Fore
        colorama.init()
        
        with open(settings_file_path, 'r') as file:
            settings = json.load(file)

            if text is None:
                text = 'Cristal'
            if lang is None:
                lang = settings['lang']['file-lang']
            if name is None:
                name = 'CristalAudio_'

            if file_path is None:
                file_path = utils.Utils.get_path_dir('Documents')
            if destination is None:
                destination = settings['outputs']['output-dir'] + 'audio\\'

            try:
                print('Elaborazione in corso...')
                tts = gTTS(text=text, lang=lang)
                n = 1
                for file in os.listdir(destination):
                    if file == f'{name}{n}.mp3':
                        n += 1
                file_name = f'{name}{n}.mp3'
                os.chdir(destination)
                tts.save(file_name)
            except FileNotFoundError:
                print(f'{Fore.RED}La directory {destination} non esiste{Fore.RESET}')
        
run( ['SPEECH', '--AUDIO', '--FILE'] ,'Test',r'C:\Users\HP\Desktop\Cristal\Cristal\source\users\Test\settings.json')