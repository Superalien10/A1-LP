import requests
import datetime
from urllib.parse import urlencode
import base64
import numpy as np
import pandas as pd

import busca_spotify as spo
import busca_discografia_2 as disco

def encontrar_musica(musica, album, artista):
    resposta = spo.spotify.search(query=musica, search_type="track")
    resultado = []
    try:
        for opcao in resposta["tracks"]["items"]:
            if opcao==None:
                print("\n\n ok \n\n")
            #elif opcao["name"].lower()==album.lower() and opcao["artists"][0]["name"].lower()==artista.lower():
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
        return fonte[0]["duration_ms"]




artista = disco.recolher_artista()
documento = disco.buscar_documento(artista)
albuns = disco.buscar_albuns(documento)
duracao = []
popularidade = []
visualizacoes = disco.buscar_views(documento)
letra = disco.buscar_letra(documento)

for album in albuns:
    for musica in albuns[album]:
        fonte = encontrar_musica(musica, album, artista)
        duracao.append(buscar_duracao(fonte))
        popularidade.append(buscar_popularidade(fonte))
dados = {"Duração":duracao, "Popularidade":popularidade, "Visualizações": visualizacoes, "Letra":letra}



#Multi-índice

indices = []
for album in albuns:
    for musica in albuns[album]:
        indices.append((album, musica))
#print(indices)
index = pd.MultiIndex.from_tuples(indices, names=["Álbum", "Música"])
print(dados)
print(index)
try:
    tabelinha = pd.DataFrame(dados, index=index)
except:
    print(dados)
    for array in dados:
        print("Ahhh", dados[array], "\n", len(dados[array]))
    tabelinha=pd.DataFrame(dados)
print(tabelinha)
nome = artista.replace(" ", "-")
tabelinha.to_csv(f"dataframe_{nome}.csv", encoding="utf-8")

