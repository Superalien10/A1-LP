import requests as r
from bs4 import BeautifulSoup as b
import pandas as pd

def recolher_artista():
    artista = input("Me indique uma banda ou um músico. \n").lower().replace(" ", "-")
    return artista

#A função buscar_documento() recolhe do usuário uma string e faz uma busca por uma página de discografia do site letras.mus.br referente a essa string.
def buscar_documento(artista):
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

#A função buscar_letra() recebe um documento, coleta links para páginas referentes às músicas, transforma esses sites em documentos e coleta deles as letras das músicas. 
def buscar_letra(documento):
    letras = []
    for part in documento.find_all("a", attrs={"class":"bt-play-song"}):
        musica_link = part.attrs.get("href")
        musica_doc=b(r.get(f"https://www.letras.mus.br{musica_link}").text, "html.parser")
        letra = musica_doc.find_all("div", attrs={"class":"cnt-letra p402_premium"})
        letras.append(letra)
    return letras
    #Todas as letras são mantidas no seu formato de html e adicionadas a uma lista. Essa lista é retornada ao final da função.

def buscar_views(documento):
    views = []
    for part in documento.find_all("a", attrs={"class":"bt-play-song"}):
        musica_link = part.attrs.get("href")
        musica_doc=b(r.get(f"https://www.letras.mus.br{musica_link}").text, "html.parser")
        try:
            view = musica_doc.find("div", attrs={"class":"cnt-info_exib"}).b.text
        except AttributeError:
            views.append(-1)
        views.append(view)
    return views

#print(buscar_views(buscar_documento("ed sheeran")))
