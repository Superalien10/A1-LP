import pandas as pd
import requests as r
from bs4 import BeautifulSoup as b

import sys

sys.path.insert(0, "..")

import busca_discografia_2 as disco

df = pd.read_csv('../dataframe_seu-jorge.csv', index_col=["Álbum","Música"])
print(df.head())
