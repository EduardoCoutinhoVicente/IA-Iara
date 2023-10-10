import yaml
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import LSTM, Dense, Embedding
from tensorflow.keras.utils import to_categorical 

data = yaml.safe_load(open('nlu\\train.yml', 'r', encoding='utf-8').read())
# vai armazenar as entradas ee saidas
inputs, outputs = [], []

for command in data['command']:
    inputs.append(command['input'].lower())
    outputs.append('{}|{}'.format(command['entity'], command['action']))


# Processart texto: palavras, caracteres, bytes, sub-palavras




max_seq = max([len(bytes(x.encode('utf-8')))for x in inputs])


print('Maior seq:', max_seq)

# criar o dataset one-hot (números de exemplos, tamanhos da seq, num caracteres) one-hot"
# criar o dataset disperso (números de exemplos, tamanhos da seq)

#Input Data one-hot encoding
input_data = np.zeros((len(inputs), max_seq, 256),dtype='float32')
for i, inp in enumerate(inputs):
    for k, ch in enumerate(bytes(inp.encode('utf-8'))):
        input_data[i, k, int(ch)] = 1.0



#Input data parse
        
#input_data = np.zeros((len(inputs), max_seq), dtype='int32')    

#for i, input in enumerate(inputs):
#    for k, ch in enumerate(input):
#        input_data[i, k] =chr2idx[ch]
        

#Output Data

labels = set(outputs)

fwrite = open('labels.txt','w',encoding='utf-8')

label2idx = {}
idx2label = {}

for k, label in enumerate(labels):
    label2idx[label] = k
    idx2label[k] = label
    fwrite.write(label + '\n')
fwrite.close()
    
output_data=[]

for output in outputs:
    output_data.append(label2idx[output])    

output_data = to_categorical(output_data, len(output_data))
        
print(output_data[0])        

model = Sequential()

model.add(LSTM(128))
model.add(Dense(len(output_data), activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])


model.fit(input_data,output_data,epochs=512)

#Salvar model
model.save('model.h5')#h5 e um tipode arquivo

#Vai classificar texto em uma entidade
def classify(text):
    #Criar um array de entrada(arrat de zeros)
    x = np.zeros((1, 50, 256), dtype='float32')
    
    # Preencher o array com dados do texto
    for k, ch in enumerate(bytes(text.encode('utf-8'))):
        x[0, k, int(ch)]=1.0
        
    # Fazer  a previsão    
    out = model.predict(x)    
    idx = out.argmax()
    print(idx2label[idx])
    
#while True:
#   text = input("Digite algo: ")
#    classify(text)
# print(inputs)
# print(outputs)
