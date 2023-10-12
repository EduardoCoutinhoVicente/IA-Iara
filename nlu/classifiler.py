from tensorflow.keras.models import load_model
import numpy as np



# Carregando o modelo pré-treinado
model = load_model('model.keras')

# Lendo as etiquetas das entidades a partir do arquivo de etiquetas
labels = open('labels.txt', 'r', encoding='utf-8').read().split('\n')

# Mapeando etiquetas para índices e vice-versa
label2idx = {}
idx2label = {}

for k, label in enumerate(labels):
    label2idx[label] = k
    idx2label[k] = label

# Função para classificar o texto em uma entidade
def classify(text):
    # Criar um array de entrada (array de zeros)
    x = np.zeros((1, 24, 256), dtype='float32')
    
    # Preencher o array com dados do texto
    for k, ch in enumerate(bytes(text.encode('utf-8'))):
        x[0, k, int(ch)] = 1.0
        
    # Fazer a previsão
    out = model.predict(x)
    
    # Encontrar o índice da etiqueta com maior probabilidade
    idx = out.argmax()
    
    # Retornar a etiqueta correspondente ao índice
    return idx2label[idx]

# Laço infinito para testar a função classify
#while True:
#    text = input('Digite algo: ')
#    print(classify(text))
