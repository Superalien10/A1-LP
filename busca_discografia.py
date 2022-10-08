import requests as r
from bs4 import BeautifulSoup as b
import pandas as pd

#A função buscar_documento() recolhe do usuário uma string e faz uma busca por uma página de discografia do site letras.mus.br referente a essa string.
def buscar_documento():
    artista = input("Me indique uma banda ou um músico. \n").lower().replace(" ", "-")
    link = f"https://www.letras.mus.br/{artista}/discografia/"
    pagina = r.get(link).text
    documento = b(pagina, "html.parser")
    return documento
    #A string é formatada e integrada numa nova string no padrão do site. É feita a busca pelo documento e a conversão em texto interpretado como html.
    #Por fim, é retornado o documento(variável que contém o código em html da página visada.)

