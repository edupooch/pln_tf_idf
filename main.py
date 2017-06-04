# coding=utf-8
# import nltk
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('stem')
import copy
import math
from nltk.corpus import stopwords
from nltk import wordnet
from re import compile
from nltk import stem
from doc_obj import make_doc


# MÉTODOS
def remove_stopwords(lista_palavras):
    return [palavra for palavra in lista_palavras if palavra not in stopwords.words('english')]


def reduz_ao_radical_lem(lista_palavras):
    lemmatizer = wordnet.WordNetLemmatizer()
    for i in range(len(lista_palavras)):
        lista_palavras[i] = lemmatizer.lemmatize(lista_palavras[i])
    return lista_palavras


def reduz_ao_radical_stem(palavras):
    snow = stem.SnowballStemmer('english')
    if type(palavras) is str:
        return snow.stem(palavras)
    if type(palavras) is list:
        for i in range(len(palavras)):
            palavras[i] = snow.stem(palavras[i])
    return palavras


def get_palavras(text):
    return compile('\w+').findall(text)


def pondera(tf):
    if tf > 0:
        return 1 + math.log10(tf)
    else:
        return 0


# SCRIPT
documentos = []
termos = []
for t in range(20):
    arquivo = open('arquivos/d' + str(t + 1) + '.txt', 'r')
    texto = arquivo.read()
    texto = texto.lower()
    palavras = get_palavras(texto)
    palavras = remove_stopwords(palavras)
    palavras = reduz_ao_radical_stem(palavras)
    termos = termos + palavras

    documentos.append(make_doc(arquivo.name.replace('arquivos/', ''), palavras, t))
    arquivo.close()

termos = list(set(termos))  # apenas palavras únicas

tf_file = open('matriz_tf.txt', 'w')
w_file = open('matriz_w.txt', 'w')
df_file = open('matriz_df.txt', 'w')
idf_file = open('matriz_idf.txt', 'w')
tf_idf_file = open('matriz_tf_idf.txt', 'w')

matriz_tf = [[0 for d in documentos] for t in termos]
matriz_w = copy.deepcopy(matriz_tf)
matriz_tf_idf = copy.deepcopy(matriz_tf)

for t in range(len(termos)):
    for d in range(len(documentos)):
        tf = documentos[d].palavras.count(termos[t])
        matriz_tf[t][d] = tf
        matriz_w[t][d] = pondera(tf)
    df = sum(1 for i in matriz_w[t] if i > 0)
    idf = math.log10(len(documentos)) / df

    for d in range(len(documentos)):
        matriz_tf_idf[t][d] = matriz_w[t][d] * idf

    # SALVA ARQUIVOS
    print >> tf_file, matriz_tf[t], ":", termos[t]
    print >> w_file, matriz_w[t], ":", termos[t]
    print >> df_file, df, ":", termos[t]
    print >> idf_file, idf, ":", termos[t]
    print >> tf_idf_file, matriz_tf_idf[t], ":", termos[t]

soma_file = open('soma_tfidf.txt', 'w')
soma = [0 for t in termos]
for t in range(len(termos)):
    for d in range(len(documentos)):
        soma[t] = soma[t] + matriz_tf_idf[t][d]
    print >> soma_file, soma[t], ";", termos[t]


query = ['radiology']
query = reduz_ao_radical_stem(query)
for d in range(len(documentos)):
    score = 0
    for t in range(len(query)):
        score = score + matriz_tf_idf[termos.index(query[t])][d]
    documentos[d].score = score

ranking_file = open('ranking.txt', 'w')
documentos.sort(key=lambda x: x.score, reverse=True)
print >> ranking_file, 'MY_RANK ; NOME ; PUBMED ; SCORE'
for d in range(len(documentos)):
    documentos[d].my_rank = d
    print >> ranking_file, d, ';', documentos[d].name, ';', documentos[d].pubmed_rank, ';', documentos[d].score
