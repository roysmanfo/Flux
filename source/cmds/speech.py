from gtts import gTTS
#import speech_recognition as sr
import os


# NOTE: Questa funzione non è ancora stata implementata
# NOTE: Le informazioni verranno richieste in modo separato e non tutto in una riga

# Sintassi: speech --audio [OPZIONE]             Conversione file
#           speech --audio                       Conversione testo   

# Sintassi: speech --text [OPZIONE]              Conversione file
#           speech --text                        Conversione testo

def run(cmd:list, user_name:str, settings_file_path:str):
    # NOTE: https://docs.python.org/3/tutorial/modules.html#intra-package-references
    import utils
    from colorama import Fore

    if cmd[1] == '--AUDIO' and '--TEXT' not in cmd:
        if '--FILE' in cmd:
            # .txt => .mp3
            
            lang = input('Lingua: ')
            name = input('Nome file: ')
            go_ahead = False

            while not go_ahead:
                file_path = input('Percorso file: ')
                if utils.Utils.check_if_file_exists(file_path):
                    go_ahead = True
                else:
                    print(f'{Fore.RED}Il file {file_path} non esiste{Fore.RESET}')

            text = open(file_path, 'r').read()
            fileDestination = input('Percorso destinazione: ')

            TextToSpeech.convert_to_speeck(text, lang, name, file_path ,fileDestination, settings_file_path)

        elif '--FILE' not in cmd:
            # text => .mp3
            pass


class TextToSpeech:
    def convert_to_speeck(text:str, lang:str, name:str, file_path:str, destination:str, settings_file_path:str) -> None:
        import json, colorama
        from colorama import Fore
        import utils
        colorama.init()
        

        with open(settings_file_path, 'r') as file:
            settings = json.load(file)

            if text == '':
                text = 'Cristal'
            if lang == '':
                lang = settings['lang']['file-lang']
            if name == '':
                name = 'CristalAudio_'

            if file_path == '':
                file_path = utils.Utils.get_path_dir('Documents')
            if destination == '':
                destination = settings['outputs']['output-dir'] + 'audio\\'

            try:
                print('Elaborazione in corso...')
                tts = gTTS(text=text, lang=lang)
                n = 1
                try:
                    os.makedirs(destination)
                    os.chdir(destination)
                    for file in os.listdir(destination):
                        if file == f'{name}{n}.mp3':
                            n += 1
                    file_name = f'{name}{n}.mp3'
                    if destination == settings['outputs']['output-dir'] + 'audio\\':
                        print(f'{Fore.GREEN}File creato: {file_name} in {destination}')
                except FileNotFoundError:
                    #Se la directory non esiste, verrà creata
                    os.mkdir(destination)
                    os.chdir(destination)
                    for file in os.listdir(destination):
                        if file == f'{name}{n}.mp3':
                            n += 1
                    file_name = f'{name}{n}.mp3'

                tts.save(file_name)
            except FileNotFoundError:
                print(f'{Fore.RED}La directory {destination} non esiste{Fore.RESET}')
        
run( ['SPEECH', '--AUDIO', '--FILE'] ,'Test',r'C:\Users\HP\Desktop\Cristal\Cristal\source\users\Test\settings.json')