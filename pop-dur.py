import requests
import datetime
from urllib.parse import urlencode
import base64

import busca_spotify as spo

def encontrar_musica(musica, album, artista):
    resposta = spo.spotify.search(query=musica, search_type="track")
    resultado = []
    for opcao in resposta["tracks"]["items"]:
        print(opcao["album"]["name"], "\n", opcao["artists"][0]["name"])
        if opcao["album"]["name"].lower()==album.lower() and opcao["artists"][0]["name"].lower()==artista.lower():
            resultado.append(opcao)
    assert len(resultado)==1, "Há mais de um registro de música nessas especificações."
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
