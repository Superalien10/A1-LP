#O código a seguir navega numa página de discografia de letras.mus.br, coleta e organiza num dicionário os nomes dos albuns e músicas do cantor ou banda referente ao site.

import requests as r
from bs4 import BeautifulSoup as b
import pandas as pd

#pagina = r.get("https://www.letras.mus.br/caetano-veloso/discografia/")  Esses são links de exemplo
#pagina = r.get("https://www.letras.mus.br/maiara-maraisa/discografia/")
#pagina = r.get("https://www.letras.mus.br/the-beatles/discografia/")
pagina = r.get("https://www.letras.mus.br/midnight-oil/discografia/")

pagina = pagina.text #Após pegar o html da página com requests, registramos sua versão em texto.
sopa = b(pagina, "html.parser") #Preparamos o texto para análise com uma função do bs4.
print("Começo") #Esse print e o último são para facilitar a localização do usuário ao buscar htmls muito extensos.

classe = sopa.find_all("div", attrs={"class":"album-item g-sp"}) #Com essa linha, pegamos cada div do tipo desejado, num objeto do bs4.
albuns={}
musicas=[]
for album in classe:
    song=album.find_all("div", attrs={"class":"song-name"}) #Coletamos os nomes das músicas no presente álbum(div), também num objeto do pacote bs4.
    for musica in song:
        musicas.append(musica.text) #Coletamos o nome da música em si e anexamos a uma lista.
    albuns[album.a.text]=musicas #Inserimos essa lista no dicionário com uma entrada referente ao álbum no qual as músicas estão.
    musicas=[] #Limpamos a lista para o próximo álbum.
print(albuns) #Imprimimos o dicionário com os álbuns e suas músicas.

print("FIM")
