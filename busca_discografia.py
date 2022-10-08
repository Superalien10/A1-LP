import requests as r
from bs4 import BeautifulSoup as b
import pandas as pd

#A função buscar_documento() recolhe do usuário uma string e faz uma busca por uma página de discografia do site letras.mus.br referente a essa string.
def buscar_documento():
    artista = input("Me indique uma banda ou um músico. \n").lower().replace(" ", "-")
    link = f"https://www.letras.mus.br/{artista}/discografia/"
    pagina = r.get(link).text
    documento = b(pagina, "html.parser")
    return documento
    #A string é formatada e integrada numa nova string no padrão do site. É feita a busca pelo documento e a conversão em texto interpretado como html.
    #Por fim, é retornado o documento(variável que contém o código em html da página visada.)

#A função buscar_albuns() coleta de um documento recebido(espera-se um do tipo html no formato das páginas de discografia de letras.mus.br) álbuns e músicas presentes na discografia visada.
def buscar_albuns(documento):
    albuns = {}
    musicas = []
    for album in documento.find_all("div", attrs={"class":"album-item g-sp"}):
        for musica in album.find_all("div", attrs={"class":"song-name"}):
            musicas.append(musica.text)
        albuns[album.a.text]=musicas
        musicas=[]
    return albuns
    #A coleta é feita com base na estrutura do código padrão do site, e é retornado pela função um dicionário cujas chaves são os álbuns do artista.
    #O valor de cada chave é uma lista contendo as músicas presentes no álbum.
