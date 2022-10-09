import requests as r
from bs4 import BeautifulSoup as b
import pandas as pd

def recolher_artista():
    """

    Recebe o nome de um musicista ou uma banda inseridos pelo usuário

    :return: O nome inserido em letras minúsculas
    :rtype: str
    """
    artista = input("Me indique uma banda ou um músico. \n").lower()
    return artista

def buscar_documento(artista):
    """

    Entra na página do letras.mus.br com a discografia do artista indicado e coleta o documento html da página

    :param str artista: O artista a quem pertence a discografia procurada
    :return: A página da discografia em html
    :rtype: 
    """
    artista.replace(" ", "-")
    link = f"https://www.letras.mus.br/{artista}/discografia/"
    pagina = r.get(link).text
    documento = b(pagina, "html.parser")
    return documento

def buscar_albuns(documento):
    """

    Busca no documento html os nomes de álbuns e músicas

    :param documento: Documento html
    :return: Dicionário contendo listas de músicas guardadas nos nomes de seus álbuns
    :rtype: dict
    """
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

def buscar_letra(documento):
    """

    Busca nas páginas do Letras, os versos da letra de cada música

    :param documento: Documento html
    :return: Uma lista com as letras das músicas, na ordem em que elas estão dispostas no documento
    :rtype: list
    """
    letras = []
    for part in documento.find_all("a", attrs={"class":"bt-play-song"}):
        musica_link = part.attrs.get("href")
        musica_doc=b(r.get(f"https://www.letras.mus.br{musica_link}").text, "html.parser")
        letra = musica_doc.find_all("div", attrs={"class":"cnt-letra p402_premium"})
        try:
            if len(letra[0].find_all("p")) == 1:
                letras.append(" ")
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
            letras.append(" ")
        except AttributeError:
            print("Caso 2: \n", letra)
            letras.append(" ")
    return letras


def buscar_views(documento):
    """

    Busca nas páginas do Letras, o tanto de visualizações no site de cada música
    :param documento: Documento html
    :return: Uma lista com as visualizações das músicas, na ordem em que elas estão dispostas no documento
    """ 
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


    
