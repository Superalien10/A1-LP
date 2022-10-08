import pandas as pd
import requests as r
from bs4 import BeautifulSoup as b
import sys
sys.path.insert(0, "..")
import busca_discografia_2 as disco
import copy



df = pd.read_csv('../dataframe_seu-jorge.csv', index_col=["Álbum","Música"])
documento = disco.buscar_documento("seu jorge")
albuns = disco.buscar_albuns(documento)

#Questão 3
"""
cola = []
for album in albuns:
    for musica in albuns[album]:
        cola.append(musica)

dados = {"Extra": cola}
indices = []
for album in albuns:
    for musica in albuns[album]:
        indices.append((album, musica))
index = pd.MultiIndex.from_tuples(indices, names=["Álbum", "Música"])
novo = pd.DataFrame(dados, index=index)

ordem_vis = df.sort_values(by=["Visualizações"], ascending=False)
ordem_vis = pd.concat([ordem_vis, novo], axis=1)
ordem_vis = ordem_vis.loc[:,["Extra", "Visualizações"]]
ordem_vis = ordem_vis.drop_duplicates(["Extra", "Visualizações"], keep='first')

ordem_vis.drop("Extra", axis=1, inplace=True)
mascara_desinformacao = ordem_vis["Visualizações"] != -1
ordem_vis = ordem_vis.loc[mascara_desinformacao]

mais_ouvidas = ordem_vis.head(10)
menos_ouvidas = ordem_vis.tail(10)
print("Músicas mais ouvidas: \n", mais_ouvidas, "\nMúsicas menos ouvidas: \n", menos_ouvidas)
mais_ouvidas.to_csv(f"dataframe_mais_ouvidas.csv", encoding="utf-8")
menos_ouvidas.to_csv(f"dataframe_menos_ouvidas.csv", encoding="utf-8")
"""

#Questão 1
"""
cola = []
for album in albuns:
    for musica in albuns[album]:
        cola.append(album)
dados = {"Extra-Álbum": cola}
novo = pd.DataFrame(dados, index=index)
ordem_vis = pd.concat([ordem_vis, novo], axis=1)
for album in albuns:
    mascara_album = ordem_vis["Extra-Álbum"] == album
    fim = copy.deepcopy(ordem_vis.loc[mascara_album])
    fim.dropna(inplace=True)
    fim.drop("Extra-Álbum", axis=1, inplace=True)
    fim.to_csv(f"dataframe_visualizacoes_{album}.csv", encoding="utf-8")
    print(fim)
"""


#Questão 4
cola = []
for album in albuns:
    for musica in albuns[album]:
        cola.append(musica)

dados = {"Extra": cola}
indices = []
for album in albuns:
    for musica in albuns[album]:
        indices.append((album, musica))
index = pd.MultiIndex.from_tuples(indices, names=["Álbum", "Música"])
novo = pd.DataFrame(dados, index=index)

ordem_vis = df.sort_values(by=["Duração"], ascending=False)
ordem_vis = pd.concat([ordem_vis, novo], axis=1)
ordem_vis = ordem_vis.loc[:,["Extra", "Duração"]]
ordem_vis = ordem_vis.drop_duplicates(["Extra", "Duração"], keep='first')

ordem_vis.drop("Extra", axis=1, inplace=True)
mascara_desinformacao = ordem_vis["Duração"] != -1
ordem_vis = ordem_vis.loc[mascara_desinformacao]

mais_longas = ordem_vis.head(10)
mais_curtas = ordem_vis.tail(10)
print("Músicas mais longas: \n", mais_longas, "\nMúsicas mais curtas: \n", mais_curtas)
mais_longas.to_csv(f"dataframe_mais_longas.csv", encoding="utf-8")
mais_curtas.to_csv(f"dataframe_mais_curtas.csv", encoding="utf-8")

#Questão 2

cola = []
for album in albuns:
    for musica in albuns[album]:
        cola.append(album)
dados = {"Extra-Álbum": cola}
novo = pd.DataFrame(dados, index=index)
ordem_vis = pd.concat([ordem_vis, novo], axis=1)
for album in albuns:
    mascara_album = ordem_vis["Extra-Álbum"] == album
    fim = copy.deepcopy(ordem_vis.loc[mascara_album])
    fim.dropna(inplace=True)
    fim.drop("Extra-Álbum", axis=1, inplace=True)
    fim.to_csv(f"dataframe_duração_{album}.csv", encoding="utf-8")
    print(fim)
    
#Questão 5

cola = []
for album in albuns:
    for musica in albuns[album]:
        cola.append(album)
dados = {"Álbum": cola}
indices = []
for album in albuns:
    for musica in albuns[album]:
        indices.append((album, musica))
index = pd.MultiIndex.from_tuples(indices, names=["Álbum", "Música"])
novo = pd.DataFrame(dados, index=index)

ordem_vis = df.sort_values(by=["Prêmios"], ascending=False)
ordem_vis = pd.concat([ordem_vis, novo], axis=1)
ordem_vis = ordem_vis.loc[:,["Álbum", "Prêmios"]]
print(ordem_vis)
ordem_vis = ordem_vis.drop_duplicates(["Álbum", "Prêmios"], keep='first')
print(ordem_vis)

#ordem_vis.drop("Extra-Álbum", axis=1, inplace=True)
mascara_desinformacao = ordem_vis["Prêmios"] != -1
ordem_vis = ordem_vis.loc[mascara_desinformacao]
#print(ordem_vis.columns)
#ordem_vis = ordem_vis.columns.droplevel(0)
premiadas = ordem_vis.head()
print(premiadas)
#print(pd.DataFrame(ordem_vis.columns))
premiadas.to_csv(f"dataframe_premiadas.csv", encoding="utf-8", index=False)
    
