import psutil
import os
from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx4
import json
from nlu.classifiler import classify  # Supondo que a função classify seja definida corretamente em outro módulo
import core

# Sintaxe de fala
engine = pyttsx4.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def close_program(name):
    for process in (process for process in psutil.process_iter(attrs=['name']) if process.info['name'] == name):
        process.terminate()

def evaluate(text):
    # Reconhecer entidade do texto
    entity = classify(text)

    if entity == 'time|getTime':
        speak(core.SystemInfo.get_time())  
    elif entity == 'time|getDate':
        speak(core.SystemInfo.get_date())

    # Abrir programas
    elif entity == 'notepad|open':
        speak('Abrindo o bloco de notas')
        os.system('notepad.exe')
        
    # Abrir programas
    elif entity == 'ola|gethello':
        speak(core.SystemInfo.gethello())    

    #elif entity == 'chrome|open':
    #    speak('Abrindo o Google Chrome')
    #    os.system('"C:/Program Files/Google/Chrome/Application/chrome.exe"')     

    elif entity == 'nome|nome':     
        speak('Não entendi')

    print('Text: {} Entity: {}'.format(text, entity))

# Carregar o modelo de reconhecimento de fala Vosk
model = Model('model')
rec = KaldiRecognizer(model, 16000)

# Configurar a captura de áudio com PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

try:
    while True:
        data = stream.read(2048)

        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            result = rec.Result()
            result = json.loads(result)

            if result is not None:
                text = result['text']
                evaluate(text)
except KeyboardInterrupt:
    print("Programa encerrado manualmente.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()