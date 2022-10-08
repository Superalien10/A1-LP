import requests
import datetime
from urllib.parse import urlencode
import base64
import numpy as np

import busca_spotify as spo

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
    return fonte[0]["popularity"]

def buscar_duracao(fonte):
    return fonte[0]["duration_ms"]

#Exemplo de uso
"""
fonte = encontrar_musica("Beds are burning", "Diesel and Dust", "Midnight Oil")
print(popularidade(fonte), duracao(fonte))
"""

import pandas as pd

import busca_discografia as disco

artista = disco.recolher_artista()
documento = disco.buscar_documento(artista)
albuns = disco.buscar_albuns(documento)
duracao = []
popularidade = []
letra = disco.buscar_letra(documento)
for album in albuns:
    print("album")
    for musica in albuns[album]:
        print("musica1")
        try:
            fonte = encontrar_musica(musica, album, artista)
            duracao.append(buscar_duracao(fonte))
            popularidade.append(buscar_popularidade(fonte))
        except AssertionError as error:
            print(error, "\n\n")
        print("musica2")
dados = {"Duração":duracao, "Popularidade":popoularidade, "Letra":letra}


#Multi-índice

indices = []
for album in albuns:
    for musica in albuns[album]:
        indices.append((album, musica))
#print(indices)
index = pd.MultiIndex.from_tuples(indices, names=["Álbum", "Música"])
print(dados)
print(index)
tabelinha = pd.DataFrame(dados, index=index)
print(tabelinha)
nome = artista.replace(" ", "-")
tabelinha.to_csv(f"dataframe_{nome}.csv", encoding="utf-8")
#encontrar_musica("Tiptoe", "Night Vision", "Imagine Dragons")

