from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3
import json

# Sintaxe de Voz
engine = pyttsx3.init()

# Configuração da voz (voz padrão ou outra, dependendo do sistema)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[-2].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Carregar o modelo de reconhecimento de fala Vosk
model = Model('model')
rec = KaldiRecognizer(model, 16000)

# Configurar a captura de áudio com PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
stream.start_stream()

#tratamento de erros:importante para lidaar ccom  exeções que
#possam ocorrer na execução, como erros ao iniciar o stream
#  de áudio ou erros de reconhecimento de fala. Isso ajudará 
# a tornar o código mais robusto.
try:
    while True:
        #Ajustando o tamanho do chunk(fragmento), que e usado para ler 
        #o áudiodeixar entre 1024 ou 2048
        data = stream.read(1024)# Lê um pedaço (chunk) de áudio do dispositivo de entrada
        
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

                print(text)
                speak(text)

except KeyboardInterrupt:
    print("Programa encerrado manualmente.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    # Encerrar e liberar recursos quando o programa terminar
    stream.stop_stream()
    stream.close()
    p.terminate()