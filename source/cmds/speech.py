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
            name = cmd[cmd.index('--AUDIO') + 2] if cmd[2] != '--file' else None
            filePath = cmd[cmd.index('--FILE') + 1]
            fileDestination = cmd[cmd.index('--FILE') + 2]
            text = open(filePath, 'r').read()

            TextToSpeech.convert(text, lang, name, fileDestination)
        elif '--FILE' not in cmd:
            # text => .mp3
            pass
            

class TextToSpeech:
    def convert(text:str, lang:str, name:str, file_path:str, destination:str):
        if text is None:
            text = 'Cristal'
        if lang is None:
            lang = 'it'
        if name is None:
            name = 'CristalAudio_'

        if file_path is None:
            file_path = '\Cristal\output\\audio\\'
        if destination is None:
            destination = ''


        print('Elaborazione in corso...')
        tts = gTTS(text=text, lang=lang)
        n = 1
        for file in os.listdir(destination):
            if file == f'{name}{n}.mp3':
                n += 1
        file_name = f'{name}{n}.mp3'
        os.chdir(destination)
        tts.save(file_name)
        
run(['--audio','it','Result', '--file', 'C:/Cristal/test.txt'])