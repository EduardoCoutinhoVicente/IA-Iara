import yaml
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.utils import to_categorical 

# Carregar os dados do arquivo YAML
data = yaml.safe_load(open('nlu\\train.yml', 'r', encoding='utf-8').read())

# Inicializar as listas de entradas e saídas
inputs, outputs = [], []

# Loop pelos comandos no arquivo YAML
for command in data['command']:
    # Adicionar a entrada e a saída à lista
    inputs.append(command['input'].lower())
    outputs.append('{}|{}'.format(command['entity'], command['action']))

# Processart texto: palavras, caracteres, bytes, sub-palavras

# Obter o tamanho máximo da sequência
max_seq = max([len(bytes(x.encode('utf-8')))for x in inputs])

print('Maior seq:', max_seq) # Imprimir o comprimento máximo encontrado.

# criar o dataset one-hot (números de exemplos, tamanhos da seq, num caracteres) one-hot"
# criar o dataset disperso (números de exemplos, tamanhos da seq)
# Criar o dataset one-hot para as entradas
input_data = np.zeros((len(inputs), max_seq, 256),dtype='float32')# Inicializar um array com zeros.

# Preencher o array one-hot com base nas entradas
for i, inp in enumerate(inputs):
    for k, ch in enumerate(bytes(inp.encode('utf-8'))):
        input_data[i, k, int(ch)] = 1.0# Codificar os caracteres das entradas como one-hot.

#Input data parse
# (Esta parte parece estar comentada, você pode escolher qual método usar: one-hot ou parse)       

#input_data = np.zeros((len(inputs), max_seq), dtype='int32')    
#for i, input in enumerate(inputs):
#    for k, ch in enumerate(input):
#        input_data[i, k] =chr2idx[ch]  
#Output Data

labels = set(outputs)#Aqui, o código cria um conjunto (set) a partir da lista de saídas (outputs). Isso é feito para garantir que apenas rótulos únicos sejam considerados, uma vez que um conjunto não

fwrite = open('labels.txt','w',encoding='utf-8')#O código abre um arquivo chamado 'labels.txt' para escrita e atribui o objeto de arquivo resultante à variável fwrite.

label2idx = {}
idx2label = {}

"""
Nesse bloco a baixo, o código percorre os rótulos únicos presentes no conjunto labels. Para cada rótulo, ele o associa a um índice (valor crescente de k) e armazena essa relação nos dicionários label2idx e idx2label. Além disso, ele escreve o rótulo no arquivo 'labels.txt' seguido por uma quebra de linha.
"""
for k, label in enumerate(labels):
    label2idx[label] = k
    idx2label[k] = label
    fwrite.write(label + '\n') # Escrever os rótulos em um arquivo.
    
fwrite.close()#o código fecha o arquivo 'labels.txt' após escrever todos os rótulos únicos.
    
output_data=[]

# Mapear as saídas para índices
for output in outputs:
    output_data.append(label2idx[output])    

output_data = to_categorical(output_data, len(output_data))# Converter saídas em one-hot encoding.
        
print(output_data[0]) # Imprimir a saída one-hot correspondente ao primeiro exemplo.     

model = Sequential()# Criar um modelo sequencial

model.add(LSTM(356))# Adicionar uma camada LSTM ao modelo]

# Adicionar uma camada densa (fully connected) com ativação softma
model.add(Dense(len(output_data), activation='softmax'))

# Compilar o modelo com otimizador "adam" e função de perda "categorical_crossentropy"
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])

# Treinar o modelo com os dados de entrada e saída
model.fit(input_data,output_data,epochs=356)

# Salvar o modelo em um arquivo (formato Keras)
model.save('model.keras')#keras e um tipode arquivo

# Função para classificar texto em uma entidade
def classify(text):
    # Criar um array de entrada (array de zeros)
    x = np.zeros((1, 58, 256), dtype='float32')

    # Preencher o array com dados do texto
    for k, ch in enumerate(bytes(text.encode('utf-8'))[:58]):
        x[0, k, int(ch)]=1.0
        
    # Fazer  a previsão    
    out = model.predict(x)    
    idx = out.argmax()
    print(idx2label[idx]) # Imprimir a entidade/classificação correspondente à previsão.
    
#while True:
#   text = input("Digite algo: ")
#    classify(text)
# print(inputs)
# print(outputs)
