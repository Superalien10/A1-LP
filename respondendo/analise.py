import pandas as pd
import requests as r
from bs4 import BeautifulSoup as b

import sys

sys.path.insert(0, "..")

import busca_discografia_2 as disco

df = pd.read_csv('../dataframe_seu-jorge.csv', index_col=["Álbum","Música"])
#print(df.head())

documento = disco.buscar_documento("seu jorge")
albuns = disco.buscar_albuns(documento)
cola = []
for album in albuns:
    for musica in albuns[album]:
        cola.append(musica)
#cola=pd.Series(cola)

dados = {"Extra": cola}
indices = []
for album in albuns:
    for musica in albuns[album]:
        indices.append((album, musica))
index = pd.MultiIndex.from_tuples(indices, names=["Álbum", "Música"])
novo = pd.DataFrame(dados, index=index)




ordem_vis = df.sort_values(by=["Visualizações"], ascending=False)
ordem_vis = pd.concat([ordem_vis, novo], axis=1)
ordem_vis.to_csv(f"dataframe_nome.csv", encoding="utf-8")
ordem_vis = ordem_vis.loc[:,["Extra", "Visualizações"]]
ordem_vis = ordem_vis.drop_duplicates(["Extra", "Visualizações"], keep='first')



ordem_vis.drop("Extra", axis=1, inplace=True)
mascara_desinformacao = ordem_vis["Visualizações"] != -1
ordem_vis = ordem_vis.loc[mascara_desinformacao]




mais_ouvidas = ordem_vis.head(10)
menos_ouvidas = ordem_vis.tail(10)
print(type(mais_ouvidas))
print("Músicas mais ouvidas: \n", mais_ouvidas, "\nMúsicas menos ouvidas: \n", menos_ouvidas)
mais_ouvidas.to_csv(f"dataframe_mais_ouvidas.csv", encoding="utf-8")
menos_ouvidas.to_csv(f"dataframe_menos_ouvidas.csv", encoding="utf-8")

