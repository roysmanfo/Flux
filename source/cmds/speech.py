from gtts import gTTS
import speech_recognition as sr
import os

# NOTE: https://docs.python.org/3/tutorial/modules.html#intra-package-references
# NOTE: Le informazioni verranno richieste in modo separato e non tutto in una riga

# Sintassi: speech --audio --file                Conversione file
#           speech --audio                       Conversione testo   

# Sintassi: speech --text [OPZIONE]              Conversione file
#           speech --text                        Conversione testo

def run(cmd:list, settings_file_path:str):

    from utils.utils import Utils
    from colorama import Fore
    import colorama
    colorama.init()
    # Controllo se non ci sono attributi sconosciuti
    for i in cmd:
        if '--' in i:
            does_attr_exist = Check.unknown_attribute(i)
            if does_attr_exist == False:
                Errors.unknown_attribute_error(i)
                return
    
    # Controllo se non ci sono argomenti
    if len(cmd) == 1:
        Errors.no_argument_error()
    
    # Controllo se l'utente richiede assistenza
    elif '--HELP' in cmd or '--H' in cmd and len(cmd) == 2:
        Help.help()
    elif '--MORE' in cmd and len(cmd) == 2:
        Help.more_help()

    # Controllo se l'utente vuole convertire un da testo a audio
    elif '--AUDIO' in cmd and '--TEXT' not in cmd:
        
        if '--FILE' in cmd:
            # Da file a file
            lang = input(f'{Fore.WHITE}Lingua:{Fore.BLUE} ')
            name = input(f'{Fore.WHITE}Nome file:{Fore.BLUE} ')
            go_ahead = False

            while not go_ahead:
                file_path = input(f'{Fore.WHITE}Percorso file:{Fore.BLUE} ')
                if Utils.check_if_file_exists(file_path):
                    go_ahead = True
                else:
                    print(f'{Fore.RED}Il file {file_path} non esiste{Fore.RESET}')

            text = open(file_path, 'r').read()
            fileDestination = input(f'{Fore.WHITE}Percorso destinazione:{Fore.BLUE} ')

            Convert.to_speech(text, lang, name, fileDestination, settings_file_path)

        elif '--FILE' not in cmd:
            # Da testo a file
            lang = input(f'{Fore.WHITE}Lingua:{Fore.BLUE} ')
            name = input(f'{Fore.WHITE}Nome file:{Fore.BLUE} ')

            text = input(f'{Fore.WHITE}Testo:{Fore.BLUE} ')
            
            Convert.to_speech(text, lang, name, '', settings_file_path)

    if '--TEXT' in cmd and '--AUDIO' not in cmd: 
        # NOTE: Questa parte non è ancora stata ne finita, ne implementata per problemi tecnici

        if '--FILE' in cmd:
            # Salva in un il file
            lang = input(f'{Fore.WHITE}Lingua:{Fore.BLUE} ')
            name = input(f'{Fore.WHITE}Nome file:{Fore.BLUE} ')

            fileDestination = input(f'{Fore.WHITE}Percorso destinazione:{Fore.BLUE} ')
            save_as_file = True

            Convert.co_text(lang, name, fileDestination, settings_file_path, save_as_file)
        elif '--FILE' not in cmd:
            # Stamperà il testo a schermo
            
            lang = input(f'{Fore.WHITE}Lingua:{Fore.BLUE} ')
            name, fileDestination = '', ''
            save_as_file = False

            Convert.to_text(lang, name, fileDestination, settings_file_path, save_as_file)

class Convert:
    def to_speech(text:str, lang:str, name:str, destination:str, settings_file_path:str) -> None:
        """
        Text to Speech
        """
        import json, colorama
        from colorama import Fore
        colorama.init()
        

        with open(settings_file_path, 'r') as file:
            settings = json.load(file)
            if text == '':
                text = 'Cristal'
            if lang == '':
                lang = settings['lang']['file-lang']
            if name == '':
                name = 'CristalAudio_'
            if destination == '':
                destination = settings['outputs']['audio']

            try:
                print(f'{Fore.WHITE}Elaborazione in corso...')
                tts = gTTS(text=text, lang=lang)
                n = 1
                try:
                    courent_dir = os.getcwd()
                    #os.makedirs(destination)
                    os.chdir(str(destination))
                    for file in os.listdir(destination):
                        if file == f'{name}{n}.mp3':
                            n += 1
                    file_name = f'{name}{n}.mp3'
                   
                except FileNotFoundError:
                    #Se la directory non esiste, verrà creata
                    courent_dir = os.getcwd()
                    os.makedirs(destination)
                    os.chdir(destination)
                    for file in os.listdir(destination):
                        if file == f'{name}{n}.mp3':
                            n += 1
                    file_name = f'{name}{n}.mp3'

                tts.save(file_name)
                
                if destination == settings['outputs']['audio']:
                        print(f'{Fore.GREEN}File creato: {file_name} in {destination}')

                os.chdir(courent_dir)
            except FileNotFoundError:
                print(f'{Fore.RED}La directory {destination} non esiste{Fore.RESET}')

    def to_text(lang:str, name:str, destination:str, settings_file_path:str, save_as_file:bool) -> None:
        """
        Speech to Text
        """
        import json, colorama
        from colorama import Fore
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

                if save_as_file:
                    courent_dir = os.getcwd()
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
                    os.chdir(courent_dir)
                else:
                    print(f'{Fore.CYAN}Testo:\n\n{text}{Fore.RESET}')
                
            except sr.UnknownValueError:
                print(f'{Fore.RED}Errore nella registrazione{Fore.RESET}')
            
        except Exception as e:
            print(e)
            print(f'{Fore.RED}Errore sconosciuto{Fore.RESET}')

class Check:
    """
    Diverse funzioni che eseguono controlli 
    """
    def unknown_attribute(attribute) -> bool:
        """
        Controlla se un attributo esiste
        """
        attrs = ['--AUDIO', '--TEXT', '--FILE', '--HELP','--H','--MORE']
        if attribute not in attrs:
            return False
        else:
            return True

class Errors:
    """
    Tutti gli errori che possono verificarsi, verranno gestiti qua
    """
    def unknown_attribute_error(attribute:str) -> None:
        import colorama
        from colorama import Fore
        colorama.init()
        print(f'{Fore.RED}Attributo {attribute} non esiste{Fore.RESET}')
        return

    def no_argument_error() -> None:
        import colorama
        from colorama import Fore
        colorama.init()
        print(f'{Fore.RED}Nessun argomento fornito{Fore.RESET}')
        return
    
    def wrong_argument_error(cmd:list) -> None:
        import colorama
        from colorama import Fore
        colorama.init()
        print(f'{Fore.RED}Errore: argomento non valido{Fore.RESET}')
        return

class Help:
    """
    Assistenza utente
    """
    def help() -> None:
        """
        Informazioni utili all'utente per usare il comando
        """
        import colorama
        from colorama import Fore
        colorama.init()
        
        print(f'{Fore.MAGENTA}Speech\n{Fore.RESET}')
        print('Permette di convertire un testo in audio')
        print('Se non viene fornito alcun attributo, il programma ti chiedera\' di fornirlo sul momento')
        print(f'{Fore.WHITE}Sintassi: speech --AUDIO [OPZIONE] | speech --TEXT [OPZIONE] | speech [OPZIONE]{Fore.RESET}')
        print(f'{Fore.WHITE}OPZIONI:\n{Fore.RESET}')
        print(f'{Fore.WHITE}\t--HELP:\t\tVisualizza questo messaggio{Fore.RESET}')
        print(f'{Fore.WHITE}\t--FILE:\t\tPermette di convertire un intero file di testo in un file audio{Fore.RESET}')
        print(f'{Fore.WHITE}\t--MORE:\t\tPermette di ottenere più informazioni sul funzionamento di speech{Fore.RESET}')

    def more_help() -> None:
        """
        Ulteriori informazioni sul funzionamento di speech
        """
        import colorama
        from colorama import Fore
        colorama.init()
        
        print(f'{Fore.MAGENTA}Speech - More Help\n{Fore.RESET}')
        print(f'{Fore.WHITE}Speech è un comando che permette di convertire un testo in audio o viceversa.{Fore.RESET}')
        print(f'{Fore.WHITE}\nIl comando è composto da due attributi: --AUDIO e --TEXT.{Fore.RESET}')
        print(f'{Fore.WHITE}Il primo attributo permette di convertire un testo in audio, mentre il secondo permette di convertire un audio in testo.{Fore.RESET}')
        print(f'{Fore.WHITE}Se oltre a uno degli attributi precedi, si inserisce l\'attributo --FILE, l\'output sarà memorizzato su un file{Fore.RESET}')
        print(f'{Fore.WHITE}Se non viene fornito alcun attributo, il programma ti chiedera\' di fornirlo sul momento{Fore.RESET}')
        print(f'{Fore.WHITE}\nQuando vengono chieste informazioni aggiuntive per l\'enecuzione della conversione, se fornite, verranno usati i valori di default{Fore.RESET}')
        print(f'{Fore.CYAN}Esempio: speech --audio --file + non fornisco il nome del file finale => il nome del file sarà CristalAudio_*{Fore.RESET}')
        print(f'{Fore.CYAN}Esempio: speech --text --file + non fornisco la destinazione => il file si troverà in */Documents/Cristal/[nome utente]/output/text/{Fore.RESET}')
#run( ['SPEECH', '--TEXT', '--FILE'],r'C:\Users\HP\Desktop\Cristal\Cristal\source\users\Test\settings.json')