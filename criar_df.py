import requests
import datetime
from urllib.parse import urlencode
import base64
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as b
import re
import copy

import busca_spotify as spo
import busca_discografia as disco

#Essa função pesquisa uma música na API do Spotify e identifica os resultados que correspondem ao álbum e ao artista inseridos nos parâmetros.
#Todas as respostas do Spotify que corresponderem ao artista e ao álbum são anexadas a uma lista.
#É assertado que só há uma opção de resposta válida. Caso não, um aviso é impresso e o programa segue.
#Se ao fim da seleção, a lista de resultado estiver vazia, é inserido o -1 padrão, que no dataframe indica que a informação não está disponível.
#Se o objeto retornado pela busca não tiver as chave solicitadas, é anexado -1.
def encontrar_musica(musica, album, artista):
    x=0
    y=0
    resposta = spo.spotify.search(query=musica, search_type="track")
    resultado = []
    try:
        for opcao in resposta["tracks"]["items"]:
            if opcao==None:
                print("\n\n ok \n\n")
            elif opcao["artists"][0]["name"].lower()==artista.lower():
                resultado.append(opcao)
        if len(resultado)==0:
            resultado.append(-1)
    except KeyError:
        resultado.append(-1)
        print(resultado)
    return resultado
    #A função retorna a lista resultado.

#A função busca_popularidade recebe uma lista fonte. Caso seu conteúdo seja -1, ela repassa -1. Caso contrário, será um dicionário, do qual a função coleta a popularidade da música e a devolve.
def buscar_popularidade(fonte):
    popularidade = []
    if fonte[0]==-1:
        return -1
    else:
        return fonte[0]["popularity"]
    #A função retorna um número inteiro entre menos um e cem, inclusos.

#A função busca_duracao recebe uma lista fonte. Caso seu conteúdo seja -1, ela repassa -1. Caso contrário, será um dicionário, do qual a função coleta a duracao em milisegundos da música, converte em segundos e a devolve.
def buscar_duracao(fonte):
    if fonte[0]==-1:
        return -1
        #print("I")
    else:
        mili=fonte[0]["duration_ms"]
        #print(mili)
        return float(mili/1000)
    #A função retorna um número decimal.
    
def criar_multiindex(albuns):
    indices = []
    for album in albuns:
        for musica in albuns[album]:
            indices.append((album, musica))
    index = pd.MultiIndex.from_tuples(indices, names=["Álbum", "Música"])
    return index


def buscar_premios(albuns):
    num=0
    premios = []
    posicao=0
    pagina_premios = requests.get("https://pt.wikipedia.org/wiki/Seu_Jorge").text
    documento_premios = b(pagina_premios, "html.parser")
    alb_prem = copy.deepcopy(albuns)
    for album in albuns:
        alb_prem[album].append(album)
    premiados = []
    for tabela in documento_premios.find_all("table", attrs={"class":"wikitable"}):
        linhas = tabela.find_all("tr")
        for element in linhas:
            element = element.find_all("td")
            if len(element)>0:
                if element[-1].text == "Venceu\n":
                    indicado = element[-2].text
                    indicado = indicado.replace(",", "")
                    indicado = indicado.replace("\n", "")
                    premiados.append(indicado)
    for album in alb_prem:
        for premio in premiados:
            for item in albuns[album]:
                item.replace(",", "")
                item.replace(" ", "*")
                item = "^"+item
                if re.search(item,premio):
                    num+=1
        premios.append(num)
        num=0
    premios_final = []
    for album in alb_prem:
        qual = len(alb_prem[album])-1
        while qual > 0:
            qual-=1
            premios_final.append(premios[posicao])
        posicao+=1
    return premios_final

def criar_dados(duracao, popularidade, visualizacoes, letra, premios):
    dados = {"Duração":duracao, "Popularidade":popularidade, "Visualizações": visualizacoes, "Letra":letra, "Prêmios": premios}
    return dados


def criar_df():
    artista = disco.recolher_artista()
    documento = disco.buscar_documento(artista)
    albuns = disco.buscar_albuns(documento)
    duracao = []
    popularidade = []
    for album in albuns:
        for musica in albuns[album]:
            fonte = encontrar_musica(musica, album, artista)
            duracao.append(buscar_duracao(fonte))
            popularidade.append(buscar_popularidade(fonte))
    visualizacoes = disco.buscar_views(documento)
    letra = disco.buscar_letra(documento)
    premios = buscar_premios(albuns)
    indice = criar_multiindex(albuns)
    print(indice)
    dados = criar_dados(duracao, popularidade, visualizacoes, letra, premios)
    tabelinha = pd.DataFrame(dados, index=indice)
    """except:
        print(dados)
        for atributo in dados:
            print("Ahhh", dados[atributo], "\n", len(dados[atributo]))
        tabelinha=pd.DataFrame(dados)
    tabelinha = tabelinha.astype({'Visualizações':'int'})"""
    print(tabelinha)
    nome = artista.replace(" ", "-")
    tabelinha.to_csv(f"dataframe_{nome}.csv", encoding="utf-8")



criar_df()

print("deu")











