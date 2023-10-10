from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3
import json
import core
from nlu.classifiler import classify

# Sintaxe de fala
engine = pyttsx3.init()

# Configuração da voz (voz padrão ou outra, dependendo do sistema)
voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[-3].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


def evaluate(text):
    # Reconhecer entidade do texto
    entity = classify(text)
    if entity == 'time\\getTime':
        speak(core.SystemInfo.get_time())  
    elif entity == 'time\getDate':
        speak(core.SystemInfo.get_date())

    # abrir programas
    elif entity == 'open\notepad':
         speak('Abrindo o bloco de notas')
         os.system('notepad.exe ')

    print('Text: {} Entity: {}'.format(text, entity))#mostra o texto ouvido

    #speak(text)#fala o texto ouvido



# Carregar o modelo de reconhecimento de fala Vosk
model = Model('model')
rec = KaldiRecognizer(model, 16000)

# Configurar a captura de áudio com PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

#tratamento de erros:importante para lidaar ccom  exeções que
#possam ocorrer na execução, como erros ao iniciar o stream
#  de áudio ou erros de reconhecimento de fala. Isso ajudará 
# a tornar o código mais robusto.
try:
    #Loop do reconhecimento de fala 
    while True:
        #Ajustando o tamanho do chunk(fragmento), que e usado para ler 
        #o áudiodeixar entre 1024 ou 2048
        data = stream.read(2048)# Lê um pedaço (chunk) de áudio do dispositivo de entrada
        
        # Verificar se não há mais dados de áudio para ler (fim do fluxo)
        if len(data) == 0:
            break

        # Enviar o chunk para o reconhecimento de fala
        if rec.AcceptWaveform(data):
            result = rec.Result()
            result = json.loads(result)

            # Imprimir o texto reconhecido e reproduzi-lo em voz
            if result is not None:
                text = result['text']
                evaluate(text)
        
                
            

except KeyboardInterrupt:
    print("Programa encerrado manualmente.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    # Encerrar e liberar recursos quando o programa terminar
    stream.stop_stream()
    stream.close()
    p.terminate()
