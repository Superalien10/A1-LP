import requests as r
from bs4 import BeautifulSoup as b
import pandas as pd

def recolher_artista():
    artista = input("Me indique uma banda ou um músico. \n").lower()
    return artista

#A função buscar_documento() recolhe do usuário uma string e faz uma busca por uma página de discografia do site letras.mus.br referente a essa string.
def buscar_documento(artista):
    artista.replace(" ", "-")
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
        album = album.a.text
        album = album.replace(":", "")
        albuns[album]=musicas
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
        try:
            #print("Caso 1: \n", letra[0].text)
            if len(letra[0].find_all("p")) == 1:
                #print("a\nr\nr\no\nz\n")
                letras.append(-1)
            else:
                novo = ""
                anterior = ""
                for caractere in letra[0].text:
                    if caractere == caractere.lower():
                        novo+=caractere
                        anterior = caractere
                    elif anterior != " ":
                        novo = novo + " " + caractere
                        anterior = caractere
                    else:
                        novo+=caractere
                letras.append(novo)
                #print(letra)
        except IndexError:
            print("Caso 2: \n", letra)
            letras.append(-1)
        except AttributeError:
            print("Caso 2: \n", letra)
            letras.append(-1)
    return letras
    #Todas as letras são mantidas no seu formato de html e adicionadas a uma lista. Essa lista é retornada ao final da função.

#def busca_duração

def buscar_views(documento):
    views = []
    for part in documento.find_all("a", attrs={"class":"bt-play-song"}):
        musica_link = part.attrs.get("href")
        musica_doc=b(r.get(f"https://www.letras.mus.br{musica_link}").text, "html.parser")
        try:
            view = musica_doc.find("div", attrs={"class":"cnt-info_exib"}).b.text
            view = view.replace(".", "")
            view = int(view)
            views.append(view)
        except AttributeError:
            views.append(-1)
    return views

