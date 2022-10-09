import pandas as pd
import requests as r
from bs4 import BeautifulSoup as b
import sys
sys.path.insert(0, "..")
import busca_discografia as disco
from criar_df import criar_multiindex
import copy


def buscando_albuns(documento):
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
            musicas.append(musica.txt)
        album = album.a.text
        album = album.replace(":", "")
        albuns[album]=musicas
        musicas=[]
    return albuns


def col_extra(df, documento, col):
    """

    Adiciona uma coluna ao df, que corresponde a um dos níveis do multi-índice

    :param pandas.Dataframe df: Dataframe que receberá anexo
    :param documento: Documento html fonte de dados
    :param str col: Nome da coluna a ser criada, que indica sua origem
    :return: Novo dataframe
    :rtype: pandas.DataFrame
    """
    albuns = disco.buscar_albuns(documento)
    index = criar_multiindex(albuns)
    if col == "Extra-Álbum":
        musica_album = []
        for album in albuns:
            for musica in albuns[album]:
                musica_album.append(album)
        dados = {"Extra-Álbum": musica_album}
        novo = pd.DataFrame(dados, index=index)
        df = pd.concat([df, novo], axis=1)
        return df
    elif col == "Extra-Música":
        musica_musica = []
        for album in albuns:
            for musica in albuns[album]:
                musica_musica.append(musica)
        dados = {"Extra-Música": musica_musica}
        novo = pd.DataFrame(dados, index=index)
        df = pd.concat([df, novo], axis=1)
        return df
    else:
        album_album = []
        for album in albuns:
            for musica in albuns[album]:
                album_album.append(album)
        dados = {"Extra-Álbum2": album_album}
        novo = pd.DataFrame(dados, index=album_album)
        df = pd.concat([df, novo], axis=1)
        return df

    
def criar_album_vis():
    """

    Cria um dataframe ordenado pelas visualizações, para cada álbum

    """
    df = pd.read_csv('../dataframe_seu-jorge.csv', index_col=["Álbum","Música"])
    documento = disco.buscar_documento("seu jorge")
    albuns = buscando_albuns(documento)
    ordem_vis = col_extra(df, documento, "Extra-Álbum")
    for album in albuns:
        mascara_album = ordem_vis["Extra-Álbum"] == album
        album_vis = copy.deepcopy(ordem_vis.loc[mascara_album])
        album_vis.dropna(inplace=True)
        mascara_desinformacao = album_vis["Visualizações"] != -1
        album_vis = album_vis.loc[mascara_desinformacao]
        album_vis.drop("Extra-Álbum", axis=1, inplace=True)
        album_vis = album_vis.sort_values(by=["Visualizações"], ascending=False)
        album_vis = album_vis.loc[:,["Visualizações"]]
        album_vis.to_csv(f"dataframe_visualizacoes_{album}.csv", encoding="utf-8")
        print(album_vis)


def criar_album_dur():
    """

    Cria um dataframe ordenado pela duração, para cada álbum
    """
    df = pd.read_csv('../dataframe_seu-jorge.csv', index_col=["Álbum","Música"])
    documento = disco.buscar_documento("seu jorge")
    albuns = buscando_albuns(documento)
    ordem_dur = col_extra(df, documento, "Extra-Álbum")
    for album in albuns:
        mascara_album = ordem_dur["Extra-Álbum"] == album
        album_dur = copy.deepcopy(ordem_dur.loc[mascara_album])
        mascara_desinformacao = album_dur["Duração"] != -1
        album_dur = album_dur.loc[mascara_desinformacao]
        album_dur.dropna(inplace=True)
        album_dur.drop("Extra-Álbum", axis=1, inplace=True)
        album_dur = album_dur.sort_values(by=["Duração"], ascending=False)
        album_dur = album_dur.loc[:,["Duração"]]
        album_dur.to_csv(f"dataframe_duração_{album}.csv", encoding="utf-8")
        print(album_dur)



def criar_musica_vis():
    """

    Cria um dataframe com as músicas mais visualizadas e outro com as menos
    """
    df = pd.read_csv('../dataframe_seu-jorge.csv', index_col=["Álbum","Música"])
    documento = disco.buscar_documento("seu jorge")
    albuns = buscando_albuns(documento)
    ordem_vis = col_extra(df, documento, "Extra-Música")
    ordem_vis = ordem_vis.sort_values(by=["Visualizações"], ascending=False)
    ordem_vis = ordem_vis.loc[:,["Extra-Música", "Visualizações"]]
    ordem_vis = ordem_vis.drop_duplicates(["Extra-Música", "Visualizações"], keep='first')
    ordem_vis.drop("Extra-Música", axis=1, inplace=True)
    mascara_desinformacao = ordem_vis["Visualizações"] != -1
    ordem_vis = ordem_vis.loc[mascara_desinformacao]
    mais_ouvidas = ordem_vis.head(10)
    menos_ouvidas = ordem_vis.tail(10)
    mais_ouvidas.to_csv(f"dataframe_mais_ouvidas.csv", encoding="utf-8")
    menos_ouvidas.to_csv(f"dataframe_menos_ouvidas.csv", encoding="utf-8")
    print("Músicas mais ouvidas: \n", mais_ouvidas, "\nMúsicas menos ouvidas: \n", menos_ouvidas)



def criar_musica_dur():
    """

    Cria um dataframe com as músicas mais longas e outro com as mais curtas
    """
    df = pd.read_csv('../dataframe_seu-jorge.csv', index_col=["Álbum","Música"])
    documento = disco.buscar_documento("seu jorge")
    albuns = buscando_albuns(documento)
    ordem_dur = col_extra(df, documento, "Extra-Música")
    ordem_dur = ordem_dur.sort_values(by=["Duração"], ascending=False)
    ordem_dur = ordem_dur.loc[:,["Extra-Música", "Duração"]]
    ordem_dur = ordem_dur.drop_duplicates(["Extra-Música", "Duração"], keep='first')
    ordem_dur.drop("Extra-Música", axis=1, inplace=True)
    mascara_desinformacao = ordem_dur["Duração"] != -1
    ordem_dur = ordem_dur.loc[mascara_desinformacao]
    mais_longas = ordem_dur.head(10)
    mais_curtas = ordem_dur.tail(10)
    mais_longas.to_csv(f"dataframe_mais_longas.csv", encoding="utf-8")
    mais_curtas.to_csv(f"dataframe_mais_curtas.csv", encoding="utf-8")
    print("Músicas mais longas: \n", mais_longas, "\nMúsicas mais curtas: \n", mais_curtas)



def criar_album_pre():
    """

    Cria um dataframe ordenado pelos prêmios com uma música por álbum e limitado aos top cinco
    """
    df = pd.read_csv('../dataframe_seu-jorge.csv', index_col=["Álbum"])
    documento = disco.buscar_documento("seu jorge")
    albuns = buscando_albuns(documento)
    ordem_pre = col_extra(df, documento, "Extra-Álbum2")
    ordem_pre = ordem_pre.sort_values(by=["Prêmios"], ascending=False)
    ordem_pre = ordem_pre.loc[:, ["Extra-Álbum2", "Prêmios"]]
    ordem_pre.drop_duplicates(["Extra-Álbum2", "Prêmios"], keep='first', inplace=True)
    mascara_desinformacao = ordem_pre["Prêmios"] != -1
    ordem_pre = ordem_pre.loc[mascara_desinformacao]
    ordem_pre.rename(columns={"Extra-Álbum2": "Álbum"}, inplace=True)
    premiadas = ordem_pre.head()
    premiadas.to_csv(f"dataframe_premiadas.csv", encoding="utf-8")
    print(premiadas)




def criar_album_pop():
    """

    Cria um dataframe ordenado pela popularidade, para cada álbum
    """
    df = pd.read_csv('../dataframe_seu-jorge.csv', index_col=["Álbum","Música"])
    documento = disco.buscar_documento("seu jorge")
    albuns = buscando_albuns(documento)
    ordem_pop = col_extra(df, documento, "Extra-Álbum")
    for album in albuns:
        mascara_album = ordem_pop["Extra-Álbum"] == album
        album_pop = copy.deepcopy(ordem_pop.loc[mascara_album])
        mascara_desinformacao = album_pop["Popularidade"] != -1
        album_pop = album_pop.loc[mascara_desinformacao]
        album_pop.dropna(inplace=True)
        album_pop.drop("Extra-Álbum", axis=1, inplace=True)
        album_pop = album_pop.sort_values(by=["Popularidade"], ascending=False)
        album_pop = album_pop.loc[:,["Popularidade"]]
        album_pop.to_csv(f"dataframe_popularidade_{album}.csv", encoding="utf-8")
        print(album_pop)




def criar_musica_pop():
    """

    Cria um dataframe com as músicas mais populares e outro com as menos populares
    """
    df = pd.read_csv('../dataframe_seu-jorge.csv', index_col=["Álbum","Música"])
    documento = disco.buscar_documento("seu jorge")
    albuns = buscando_albuns(documento)
    ordem_pop = col_extra(df, documento, "Extra-Música")
    ordem_pop = ordem_pop.sort_values(by=["Popularidade"], ascending=False)
    ordem_pop = ordem_pop.loc[:,["Extra-Música", "Popularidade"]]
    ordem_pop = ordem_pop.drop_duplicates(["Extra-Música", "Popularidade"], keep='first')
    ordem_pop.drop("Extra-Música", axis=1, inplace=True)
    mascara_desinformacao = ordem_pop["Popularidade"] != -1
    ordem_pop = ordem_pop.loc[mascara_desinformacao]
    mais_populares = ordem_pop.head(10)
    menos_populares = ordem_pop.tail(10)
    mais_populares.to_csv(f"dataframe_mais_populares.csv", encoding="utf-8")
    menos_populares.to_csv(f"dataframe_menos_populares.csv", encoding="utf-8")
    print("Músicas mais populares: \n", mais_populares, "\nMúsicas menos populares: \n", menos_populares)




if __name__ == '__main__':
    criar_album_vis()
    criar_album_dur()
    criar_musica_vis()
    criar_musica_dur()
    criar_album_pre()
    criar_album_pop()
    criar_musica_pop()
