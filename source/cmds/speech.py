from gtts import gTTS
import speech_recognition as sr
import os


# Sintassi: speech --audio <lang> <name> --file <filePath> <FileDestination>    Conversione file
#           speech --audio <text> <FileDestination> <lang>                      Conversione testo   

# Sintassi: speech --text <lang> <name> --file <FileDestination>                Conversione file
#           speech --text <lang> <name> <FileDestination>                       Conversione testo

def run(cmd):
    if '--audio' in cmd and '--text' not in cmd:
        if '--file' in cmd:
            # .txt => .mp3
            file = cmd[cmd.index('--file') + 1]
            print('file: ' + file)
            

class TextToSpeech:
    def convert(text = 'Cristal', lang = 'it', destination = '\\', name="CristalAudio_"):
        print('Elaborazione in corso...')
        tts = gTTS(text=text, lang=lang)
        n = 1
        for file in os.listdir(destination):
            if file == f'{name}{n}.mp3':
                n += 1
        file_name = f'{name}{n}.mp3'
        os.chdir(destination)
        tts.save(file_name)
        
run(['--audio', '--file', 'C:/test.txt'])