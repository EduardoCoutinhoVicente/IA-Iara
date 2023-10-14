import psutil
import os
from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx4
import json
from nlu.classifiler import classify  # Supondo que a função classify seja definida corretamente em outro módulo
import core

# Sintaxe de fala
engine = pyttsx4.init()# Mecanismo de texto de fala que será usado para transformar texto em fala.

# Função para sintetizar e reproduzir fala
def speak(text):#Esta é uma função que permite ao programa falar um pedaço de texto fornecido
    engine.say(text)# Aqui, o programa "guarda" o texto fornecido, para ler em voz alta.
    engine.runAndWait()#Esta linha faz com que o programa realmente leia o texto em voz alta.



# Função para avaliar e responder ao texto reconhecido
def evaluate(text):#Você pode adicionar as ações que deseja que o programa execute com base no texto que você fornecer a essa função.
    
    entity = classify(text)# Reconhecer entidade do texto

    #o programa verifica se você pediu para saber as horas. Caso recolheça ela lhe informarar as horas
    if entity == 'time|getTime':
        speak(core.SystemInfo.get_time())  
    #o programa verifica se você pediu para saber a data. Caso recolheça ela lhe informarar a data de hoje    
    elif entity == 'time|getDate':
        speak(core.SystemInfo.get_date())

    # Abrir programas
    elif entity == 'notepad|open':
        speak('Abrindo o bloco de notas')
        os.system('notepad.exe')
        
    # Verifica se voce "ola" Caso reconheça ele lhe respondera com uma saudação.
    elif entity == 'cria|getlingua':
        speak(core.SystemInfo.getlingua())    
        
    # Verifica se voce "ola" Caso reconheça ele lhe respondera com uma saudação.
    elif entity == 'ola|gethello':
        speak(core.SystemInfo.gethello())
    
    elif entity == 'nome|nome':     
        speak('Não entendi')

    #Esta linha imprime o texto de entrada e a entidade reconhecida para fins de depuração.
    print('Text: {} Entity: {}'.format(text, entity))

"""
Carregar o modelo de reconhecimento de fala Vosk,
carregando um modelo de reconhecimento de fala chamado 'model',
Esse modelo é usado para entender o que é dito no áudio.
"""
model = Model('model')

"""
criando um reconhecedor de fala Kaldi que usa o modelo carregado. 
Ele opera a uma taxa de amostragem de 16.000 amostras por segundo.
Você está preparando um programa que usa o 
modelo para ouvir e entender o que é dito com uma qualidade de som específica.
"""
rec = KaldiRecognizer(model, 16000)

# Configurar a captura de áudio com PyAudio
p = pyaudio.PyAudio()

"""
Esta parte é sobre como o microfone deve capturar o som,
como quantos canais de áudio ele usa e com que qualidade.
"""
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
stream.start_stream()

try:# Loop principal: Captura de áudio, reconhecimento e ação
    while True:
        # A cada passo do loop, o programa Captura um pequeno pedaço do áudio.
        data = stream.read(2048)
        
        #Esse pedaço de som é enviado para o programa que tenta entender o que foi dito.Se o programa conseguir entender, ele pega o que você disse e realizar ações com base no que foi reconhecido
        if len(data) == 0:
            break
    
        # faz o reconhecimento de voz e realiza ações com base no que foi reconhecido,verifica se o reconhecedor aceitou com sucesso os dados de áudio capturados na variável data.
        if rec.AcceptWaveform(data):
            #Se os dados de áudio foram aceitos com sucesso, esta linha ira obter o resultado do reconhecimento de voz
            result = rec.Result()
            #converte esses dados JSON em um formato que pode ser facilmente manipulado em Python
            result = json.loads(result)

            #verifica se o resultado do reconhecimento não está vazio
            if result is not None:
                text = result['text'] #Se o resultado não for nula,  ele pega o que foi dito e guarda na variável "text".
                evaluate(text)#Se houver um resultado válido, você extrai o texto reconhecido e chama a função evaluate para processar o texto.
                
#Se você interromper manualmente o programa, ele mostra uma mensagem dizendo que o programa foi encerrado.
except KeyboardInterrupt:
    print("Programa encerrado manualmente.")
    
#Se algo der errado no programa, ele mostra uma mensagem de erro.
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    stream.stop_stream()#Desliga a gravação de áudio.
    stream.close()    #Fecha tudo relacionado à gravação de áudio.
    p.terminate()    #Encerra o programa de gravação de áudio.