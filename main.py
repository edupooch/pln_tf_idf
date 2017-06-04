# coding=utf-8
# import nltk
# nltk.download('wordnet')
# nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk import wordnet
from re import compile


# MÉTODOS
def remove_stopwords(lista_palavras):
    return [palavra for palavra in lista_palavras if palavra not in stopwords.words('english')]


def reduz_ao_radical(lista_palavras):
    lemmatizer = wordnet.WordNetLemmatizer()
    for i in range(len(lista_palavras)):
        lista_palavras[i] = lemmatizer.lemmatize(lista_palavras[i])
    return lista_palavras


def get_palavras(texto):
    return compile('\w+').findall(texto)


# MAIN
documentos = []
termos = []
for t in range(20):
    arquivo = open('arquivos/d' + str(t + 1) + '.txt', 'r')
    texto = arquivo.read()
    texto = texto.lower()
    arquivo.close()

    documentos.append(get_palavras(texto))
    documentos[t] = remove_stopwords(documentos[t])
    documentos[t] = reduz_ao_radical(documentos[t])
    termos = termos + documentos[t]

termos = list(set(termos))  # apenas palavras únicas

f = open('matriz.txt', 'w')

matriz = [[0 for x in documentos] for y in termos]
for t in range(len(termos)):
    for d in range(len(documentos)):
        matriz[t][d] = documentos[d].count(termos[t])
    print >> f, termos[t], ":", matriz[t], '\n'
