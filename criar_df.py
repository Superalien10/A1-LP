import requests
import datetime
from urllib.parse import urlencode
import base64
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as b
import re
import copy
import sys
sys.path.insert(0, ".")
import busca_spotify as spo
import busca_discografia as disco

#Essa função pesquisa uma música na API do Spotify e identifica os resultados que correspondem ao álbum e ao artista inseridos nos parâmetros.
#Todas as respostas do Spotify que corresponderem ao artista e ao álbum são anexadas a uma lista.
#É assertado que só há uma opção de resposta válida. Caso não, um aviso é impresso e o programa segue.
#Se ao fim da seleção, a lista de resultado estiver vazia, é inserido o -1 padrão, que no dataframe indica que a informação não está disponível.
#Se o objeto retornado pela busca não tiver as chave solicitadas, é anexado -1.
def encontrar_musica(musica, album, artista):
    """

    Faz uma pesquisa na API do Spotify e retorna os resultados
    
    :param str musica: A música buscada
    :param str album: O álbum do qual a música faz parte
    :param str artista: O musicista ou banda a quem a música pertence
    :return: Os registro de música com esse nome que se enquadram no álbum e no artista
    :rtype: list
    :raise KeyError: se opcao não tiver as chaves requisitadas
    """
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

#A função busca_popularidade recebe uma lista fonte. Caso seu conteúdo seja -1, ela repassa -1. Caso contrário, será um ou mais dicionários, e a função coleta, do primeiro deles, a popularidade da música e a devolve.
def buscar_popularidade(fonte):
    """

    Busca no primeiro item de uma lista o valor da popularidade
    
    :param list fonte: Lista de resultados obtidos da função encontrar_musica()
    :return: A popularidade
    >rtype: int
    """
    if fonte[0]==-1:
        return -1
    else:
        return fonte[0]["popularity"]

#A função busca_duracao recebe uma lista fonte. Caso seu conteúdo seja -1, ela repassa -1. Caso contrário, será um ou mais dicionários, e a função coleta, do primeiro deles, a duracao em milisegundos da música, a converte em segundos e a devolve.
def buscar_duracao(fonte):
    """

    Busca no primeiro item de uma lista o valor da duração
    
    :param list fonte: Lista de resultados obtidos pela função encontrar_musica()
    :return: A duração
    >rtype: int or float
    """
    if fonte[0]==-1:
        return -1
    else:
        mili=fonte[0]["duration_ms"]
        return float(mili/1000)
    
def criar_multiindex(albuns):
    """

    Cria um multi-index composto por nomes de álbuns e músicas
    
    :param dict albuns: Dicionário no qual as chaves são álbuns de um artista, e os valores dessas chaves são listas das músicas correspondentes
    :return: Uma estrutura multi-index
    >rtype: pandas.core.indexes.multi.MultiIndex
    """
    indices = []
    for album in albuns:
        for musica in albuns[album]:
            indices.append((album, musica))
    index = pd.MultiIndex.from_tuples(indices, names=["Álbum", "Música"])
    return index


def buscar_premios(albuns):
    """

    Busca numa página da wikipédia os prêmios que o músico Seu Jorge conquistou em sua carreira musical
    
    :param dict albuns: Dicionário no qual as chaves são álbuns de um artista, e os valores dessas chaves são listas das músicas correspondentes
    :return: Uma lista com o tanto de prêmios ganhos num álbum do Seu Jorge para cada música presente no álbum. Caso o artista buscado seja outro que não ele, a série deve estar preenchida por zeros.
    >rtype: list
    """
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
    """

    Cria, a partir de listas, um dicionário

    :param list duracao: A duração em segundos de cada música, de acordo com o Spotify
    :param list popularidade: A popularidade de cada música, de 1 a 100, de acordo com o Spotify
    :param list visualizacoes: O número de visualizações da música no site letras.mus.br
    :param list letra: A letra da música, de acordo com o Letras
    :param list premios: A quantidade de prêmios recebidos pelo álbum correspondente a cada música, de acordo com a Wikipédia
    :return: Um dicionário
    :rtype: dict
    """
    dados = {"Duração":duracao, "Popularidade":popularidade, "Visualizações": visualizacoes, "Letra":letra, "Prêmios": premios}
    return dados


def criar_df():
    """

    Função central do módulo. Ela chama as outras funções e funções de outros módulos, para montar um dataframe, mostrá-lo ao usuário e salvá-lo com um arquivo .csv. Ela não retorna nada. Qualquer entrada '-1' no dataframe indica uma informação não encontrada pelo programa.
    """
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
    dados = criar_dados(duracao, popularidade, visualizacoes, letra, premios)
    tabelinha = pd.DataFrame(dados, index=indice)
    print(tabelinha)
    nome = artista.replace(" ", "-")
    tabelinha.to_csv(f"dataframe_{nome}.csv", encoding="utf-8")


if __name__ == "__main__":
    criar_df()






