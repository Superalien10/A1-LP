import requests
import datetime
from urllib.parse import urlencode
import base64
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as b
import re

import busca_spotify as spo
import busca_discografia as disco

def encontrar_musica(musica, album, artista):
    resposta = spo.spotify.search(query=musica, search_type="track")
    resultado = []
    try:
        for opcao in resposta["tracks"]["items"]:
            if opcao==None:
                print("\n\n ok \n\n")
            elif opcao["artists"][0]["name"].lower()==artista.lower():
                resultado.append(opcao)
            """print("\n\n", opcao["name"], "+", album, "\n\n", opcao["artists"][0]["name"], "+", artista)
            print("AQUI", opcao)"""
            try:
                assert len(resultado)==1, "Há mais de um registro de música nessas especificações."
            except AssertionError as error:
                 print(error, "\n\n")
            if len(resultado)==0:
                resultado.append(-1)
            return resultado
    except KeyError:
        resultado.append(-1)
        return resultado
    

def buscar_popularidade(fonte):
    if fonte[0]==-1:
        return -1
    else:
        return fonte[0]["popularity"]

def buscar_duracao(fonte):
    if fonte[0]==-1:
        return -1
    else:
        mili=fonte[0]["duration_ms"]
        #mili = float("{:.2f}".format(mili))
        return float(mili/1000)



artista = disco.recolher_artista()
documento = disco.buscar_documento(artista)
albuns = disco.buscar_albuns(documento)

duracao = []
fonte_duração = []
popularidade = []
visualizacoes = disco.buscar_views(documento)
letra = disco.buscar_letra(documento)

for album in albuns:
    for musica in albuns[album]:
        fonte = encontrar_musica(musica, album, artista)
        duracao.append(buscar_duracao(fonte))
        fonte_duração.append(fonte)
        popularidade.append(buscar_popularidade(fonte))

#Multi-índice

indices = []
for album in albuns:
    for musica in albuns[album]:
        indices.append((album, musica))
#print(indices)
index = pd.MultiIndex.from_tuples(indices, names=["Álbum", "Música"])

#Busca prêmios.

pagina = requests.get("https://pt.wikipedia.org/wiki/Seu_Jorge").text
documento = b(pagina, "html.parser")
for album in albuns:
    albuns[album].append(album)
premiados = []
for tabela in documento.find_all("table", attrs={"class":"wikitable"}):
    linhas = tabela.find_all("tr")
    for element in linhas:
        element = element.find_all("td")
        if len(element)>0:
            if element[-1].text == "Venceu\n":
                indicado = element[-2].text
                indicado = indicado.replace(",", "")
                indicado = indicado.replace("\n", "")
                premiados.append(indicado)
num=0
premios = []
for album in albuns:
    for premio in premiados:
        for item in albuns[album]:
            item.replace(",", "")
            item.replace(" ", "*")
            item = "^"+item
            if re.search(item,premio):
                num+=1
    premios.append(num)
    num=0
posicao=0
premios_final = []
for album in albuns:
    qual = len(albuns[album])-1
    while qual > 0:
        qual-=1
        premios_final.append(premios[posicao])
    posicao+=1

#Criação dos dados.
dados = {"Duração":duracao, "Popularidade":popularidade, "Visualizações": visualizacoes, "Letra":letra, "Prêmios": premios_final}



print(dados)
print(index)
try:
    tabelinha = pd.DataFrame(dados, index=index)
except:
    print(dados)
    for array in dados:
        print("Ahhh", dados[array], "\n", len(dados[array]))
    tabelinha=pd.DataFrame(dados)
tabelinha = tabelinha.astype({'Visualizações':'int'})
print(tabelinha)
nome = artista.replace(" ", "-")
tabelinha.to_csv(f"dataframe_{nome}.csv", encoding="utf-8")




