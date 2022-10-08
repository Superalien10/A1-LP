import pandas as pd
import requests as r
from bs4 import BeautifulSoup as b

import sys

sys.path.insert(0, "..")

import busca_discografia_2 as disco

df = pd.read_csv('../dataframe_seu-jorge.csv', index_col=["Álbum","Música"])
print(df.head())

documento = disco.buscar_documento("seu jorge")
albuns = disco.buscar_albuns(documento)
cola = []
for album in albuns:
    for musica in albuns[album]:
        print(musica)
        cola.append(musica)
#cola=pd.Series(cola)

dados = {"Extra": cola}
indices = []
for album in albuns:
    for musica in albuns[album]:
        indices.append((album, musica))
index = pd.MultiIndex.from_tuples(indices, names=["Álbum", "Música"])
novo = pd.DataFrame(dados, index=index)



print(df.sort_values(by=["Álbum"]))
ordem_vis = df.sort_values(by=["Visualizações"])
#novo = ordem_vis.iloc[:,"Música"]
ordem_vis = pd.concat([ordem_vis, novo], axis=1)
print(ordem_vis)
ordem_vis.to_csv(f"dataframe_nome.csv", encoding="utf-8")
#print(ordem_vis.drop_duplicates(["Música"], keep='first'))
ordem_vis = ordem_vis.loc[:,["Extra", "Visualizações"]]
print(ordem_vis)
print(ordem_vis.drop_duplicates(["Extra", "Visualizações"], keep='first'))


"""
for part in documento.find_all("a", attrs={"class":"bt-play-song"}):
        musica_link = part.attrs.get("href")
        musica_doc=b(r.get(f"https://www.letras.mus.br{musica_link}").text, "html.parser")
        try:
            view = musica_doc.find("div", attrs={"class":"cnt-info_exib"}).b.text
            #pd.to_numeric(view)
            #view = float(view)
            view = view.replace(".", "")
            view = int(view)
            print(view, type(view))
        except AttributeError:
            print("ops")
"""
