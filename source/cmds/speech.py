from gtts import gTTS
import speech_recognition as sr
import os

# NOTE: https://docs.python.org/3/tutorial/modules.html#intra-package-references
# NOTE: Questa funzione non è ancora stata implementata
# NOTE: Le informazioni verranno richieste in modo separato e non tutto in una riga

# Sintassi: speech --audio --file                Conversione file
#           speech --audio                       Conversione testo   

# Sintassi: speech --text [OPZIONE]              Conversione file
#           speech --text                        Conversione testo

def run(cmd:list, user_name:str, settings_file_path:str):

    import utils
    from colorama import Fore

    if cmd[1] == '--AUDIO' and '--TEXT' not in cmd:
        if '--FILE' in cmd:
            # Da file a file
            lang = input(f'{Fore.WHITE}Lingua:{Fore.BLUE} ')
            name = input(f'{Fore.WHITE}Nome file:{Fore.BLUE} ')
            go_ahead = False

            while not go_ahead:
                file_path = input(f'{Fore.WHITE}Percorso file:{Fore.BLUE} ')
                if utils.Utils.check_if_file_exists(file_path):
                    go_ahead = True
                else:
                    print(f'{Fore.RED}Il file {file_path} non esiste{Fore.RESET}')

            text = open(file_path, 'r').read()
            fileDestination = input(f'{Fore.WHITE}Percorso destinazione:{Fore.BLUE} ')

            TextToSpeech.convert_to_speech(text, lang, name, file_path ,fileDestination, settings_file_path)

        elif '--FILE' not in cmd:
            # Da testo a file
            lang = input(f'{Fore.WHITE}Lingua:{Fore.BLUE} ')
            name = input(f'{Fore.WHITE}Nome file:{Fore.BLUE} ')
            go_ahead = False

            while not go_ahead:
                file_path = input(f'{Fore.WHITE}Percorso file:{Fore.BLUE} ')
                if utils.Utils.check_if_file_exists(file_path):
                    go_ahead = True
                else:
                    print(f'{Fore.RED}Il file {file_path} non esiste{Fore.RESET}')

            text = input(f'{Fore.WHITE}Testo:{Fore.BLUE} ')
            fileDestination = input(f'{Fore.WHITE}Percorso destinazione:{Fore.BLUE} ')

            TextToSpeech.convert_to_speech(text, lang, name, file_path ,fileDestination, settings_file_path)

    if cmd[1] == '--TEXT' and '--AUDIO' not in cmd:   
        if '--FILE' in cmd:
            # Salva in un il file
            lang = input(f'{Fore.WHITE}Lingua:{Fore.BLUE} ')
            name = input(f'{Fore.WHITE}Nome file:{Fore.BLUE} ')
            go_ahead = False

            fileDestination = input(f'{Fore.WHITE}Percorso destinazione:{Fore.BLUE} ')
            TextToSpeech.convert_to_text(lang, name, fileDestination, settings_file_path)
        elif '--FILE' not in cmd:
            # Stamperà il testo a schermo
            pass

class TextToSpeech:
    def convert_to_speech(text:str, lang:str, name:str, file_path:str, destination:str, settings_file_path:str) -> None:
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
                destination = settings['outputs']['audio']

            try:
                print(f'{Fore.WHITE}Elaborazione in corso...')
                tts = gTTS(text=text, lang=lang)
                n = 1
                try:
                    os.makedirs(destination)
                    os.chdir(destination)
                    for file in os.listdir(destination):
                        if file == f'{name}{n}.mp3':
                            n += 1
                    file_name = f'{name}{n}.mp3'
                    if destination == settings['outputs']['audio']:
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

    def convert_to_text(lang:str, name:str, destination:str, settings_file_path:str) -> None:
        """
        Visti i problemi con pyAudio, questa funzione non è ancora stata implementata
        """
        import json, colorama
        from colorama import Fore
        import utils
        colorama.init()

        with open(settings_file_path, 'r') as file:
            settings = json.load(file)

        if lang == '':
            lang = settings['lang']['general-lang']
        if name == '':
            name = settings['file-name']['text']
        if destination == '':
            destination = settings['outputs']['text']

        try:
            
            recognizer_istance = sr.Recognizer()
            
            with sr.Microphone() as source:
                recognizer_istance.adjust_for_ambient_noise(source)
                print(f"{Fore.WHITE}In Ascolto")
                audio = recognizer_istance.listen(source)
                print('\nElaborazione in corso...')
            
            try:

                text = recognizer_istance.recognize_google(audio, language=lang)
                print(f'{Fore.GREEN}Registrazione riuscita{Fore.RESET}')

                os.makedirs(destination)
                os.chdir(destination)

                n = 1
                for file in os.listdir(destination):
                    if file == f'{name}{n}.txt':
                        n += 1
                file_name = f'{name}{n}.txt'

                with open(file_name, 'w') as file:
                    file.writelines(text)
                    print(f'{Fore.GREEN}File creato: {name}.txt in {destination}')
                
            except sr.UnknownValueError:
                print(f'{Fore.RED}Errore nella registrazione{Fore.RESET}')
        
        except Exception:
            print(f'{Fore.RED}Errore sconosciuto{Fore.RESET}')
        
run( ['SPEECH', '--TEXT', '--FILE'] ,'Test',r'C:\Users\HP\Desktop\Cristal\Cristal\source\users\Test\settings.json')