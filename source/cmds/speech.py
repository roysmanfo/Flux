from gtts import gTTS
import speech_recognition as sr
import os


# Sintassi: speech --audio <lang> <name> --file  <filePath> <FileDestination>    Conversione file
#           speech --audio <text> <FileDestination> <lang>                      Conversione testo   

# Sintassi: speech --text <lang> <name> --file <FileDestination>                Conversione file
#           speech --text <lang> <name> <FileDestination>                       Conversione testo

def run(cmd):
    if cmd[0] == '--AUDIO' and '--TEXT' not in cmd:
        if '--FILE' in cmd:
            # .txt => .mp3
            lang = cmd[cmd.index('--AUDIO') + 1]
            name = cmd[cmd.index('--AUDIO') + 2]
            filePath = cmd[cmd.index('--FILE') + 1]
            fileDestination = cmd[cmd.index('--FILE') + 2]
            text = open(filePath, 'r').read()

            TextToSpeech.convert(text, lang, name, fileDestination)
        elif '--FILE' not in cmd:
            # text => .mp3
            pass
            

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