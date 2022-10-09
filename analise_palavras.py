import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from collections import Counter
import re

# criando o dataframe com as músicas
df_seu_jorge = pd.read_csv(r'C:\Users\rodri\Downloads\Estudos\FGV\Matérias\6° Período\Linguagens de Programação\A1 LP\dataframe_seu-jorge.csv')

# definindo e atualizando as stopwords
stopwords_arquivo = open(r'C:\Users\rodri\Downloads\Estudos\FGV\Matérias\6° Período\Linguagens de Programação\A1 LP\stopwords_portugues.txt', 'r', encoding = 'utf-8')

stopwords_portugues = list(line.split(' ') for line in stopwords_arquivo.readlines())
stopwords_portugues = stopwords_portugues[0]
stopwords = set(STOPWORDS)
stopwords.update(stopwords_portugues + ['go', 's', 'n\'', '2x', 'let', 't', 'don'])

def analise_discografia(tipo):
    """

    Busca as cinco palavras mais repetidas (sem contar as stopwords) nos títulos dos álbuns, nos títulos das músicas e nas letras delas. Leva em consideração toda a discografia do autor

    :param str tipo: Escolher se vai pesquisar Álbum, Música ou Letra
    :return: As cinco palavras que mais aparecem na discografia do tipo especificado
    :rtype: tuple
    :raise NameError: Caso o nome de tipo não se refira às colunas: Álbum, Música ou Letra
    :raise KeyError: Caso o tipo não tenha as chaves requisitadas
    """

    try:
        elementos_discografia = df_seu_jorge[f'{tipo}']
        elementos_discografia = elementos_discografia.drop_duplicates()

        conteudo = ' '.join(a for a in elementos_discografia)
        conteudo = re.sub(r'[^\w]', ' ', conteudo)
        conteudo = conteudo.lower()
        conteudo = conteudo.split()

        contagem = Counter(conteudo)

        for palavra in stopwords:
            contagem.pop(palavra, None)

    except NameError as ne:
        print('NameError. Por favor, digite um valor válido! \n', ne)
    except KeyError as ke:
        print('KeyError. Valor inválido! \n', ke)
    else:
        return f'As Palavras mais comuns em {tipo} são:', contagem.most_common(5)




def palavras_musicas_album(album):
    """

    Busca as cinco palavras mais repetidas (sem contar as stopwords) nas letras de um determinado álbum do autor

    :param str album: Escolher o álbum a ser pesquisado
    :return: As cinco palavras que mais aparecem nas letras do álbum especificado
    :rtype: tuple
    :raise NameError: Caso o parâmetro não se refira a nenhum álbum do autor
    :raise KeyError: Caso o parâmetro não tenha as chaves requisitadas
    """

    try:
        df_albuns = df_seu_jorge.set_index('Álbum')
        elementos_album = df_albuns.loc[f'{album}']
        elementos_discografia = elementos_album['Letra']

        elementos_discografia = elementos_discografia.drop_duplicates()

        letras = ' '.join(a for a in elementos_discografia)
        letras = re.sub(r'[^\w]', ' ', letras)
        letras = letras.lower()
        letras = letras.split()

        contagem = Counter(letras)

        for palavra in stopwords:
            contagem.pop(palavra, None)

    except NameError as ne:
        print('NameError. Por favor, digite um valor válido! \n', ne)
    except KeyError as ke:
        print('KeyError. Valor inválido! \n', ke)
    else:
        return f'As Palavras mais comuns nas letras do álbum {album} são:', contagem.most_common(5)





def nuvem_palavras(tipo):
    """

    Busca as palavras mais frequentes (sem contar as stopwords) do tipo - sendo ele os álbuns, músicas ou letras das músicas do autor - para formar uma nuvem de palavras

    :param str tipo: Escolher se vai pesquisar Álbum, Música ou Letra
    :return: Uma nuvem de palavras com as palavras mais frequentes nos títulos dos Álbuns, das músicas e nas letras das músicas
    :rtype: wordcloud.wordcloud.WordCloud
    :raise NameError: Caso o nome de tipo não se refira às colunas: Álbum, Música ou Letra
    :raise KeyError: Caso o tipo não tenha as chaves requisitadas
    """

    try:
        elementos_discografia = df_seu_jorge[f'{tipo}']
        elementos_discografia = elementos_discografia.drop_duplicates()

        conteudo = ' '.join(a for a in elementos_discografia)

        wordcloud = WordCloud(stopwords = stopwords,
                      collocations = False,
                      background_color= 'black',
                      width = 1600, height = 800,
                      max_font_size=200, min_font_size=1).generate(conteudo)

        fig, ax = plt.subplots(figsize  = (14, 8), facecolor = 'k')
        ax.imshow(wordcloud, interpolation = 'bilinear')
        ax.set_axis_off()

    except NameError as ne:
        print('NameError. Por favor, digite um valor válido! \n', ne)
    except KeyError as ke:
        print('KeyError. Valor inválido! \n', ke)
    else:
        return wordcloud.to_file(f'{tipo}.nuvem_palavras.png')

    

def recorrencia_album_letra(album):
    """

    Verifica se o tema do título do álbum é recorrente nas letras de suas músicas

    :param str album: O nome do álbum a ser analisado
    :return: O número de vezes que o título do álbum aparece nas letras de suas músicas
    :rtype: tuple
    :raise NameError: Caso o nome do álbum não exista
    :raise KeyError: Caso o parâmetro não tenha as chaves requisitadas
    """

    contador = 0
    
    try:
        df_albuns = df_seu_jorge.set_index('Álbum')
        elementos_album = df_albuns.loc[f'{album}']
        elementos_discografia = elementos_album['Letra']

        elementos_discografia = elementos_discografia.drop_duplicates()

        letras = ' '.join(a for a in elementos_discografia)
        letras = re.sub(r'[^\w]', ' ', letras)
        letras = letras.lower()
        letras = letras.split()

        contagem = Counter(letras)

        for palavra in stopwords:
            contagem.pop(palavra, None)

        lista_palavras = list(contagem.elements())
        
        for palavra in lista_palavras:
            if palavra in album.lower():
                contador += 1

    except NameError as ne:
        print('NameError. Por favor, digite um valor válido! \n', ne)
    except KeyError as ke:
        print('KeyError. Valor inválido! \n', ke)
    else:
        return f'O número de aparições da temática de {album} em suas músicas é:', contador



def recorrencia_musica_letra(musica):
    """

    Verifica se o tema do título da música é recorrente em sua letra

    :param str musicca: O nome da música a ser analisada
    :return: O número de vezes que o título da música aparece em sua letra
    :rtype: tuple
    :raise NameError: Caso o nome da música não exista
    :raise KeyError: Caso o parâmetro não tenha as chaves requisitadas
    """

    contador = 0
    
    try:
        df_albuns = df_seu_jorge.set_index('Música')
        elementos_album = df_albuns['Letra']
        elementos_discografia = elementos_album.drop_duplicates()
        elementos_discografia = elementos_discografia.loc[f'{musica}']
        
        letras = ' '.join(elementos_discografia)
        letras = re.sub(r'[^\w]', ' ', letras)
        letras = letras.lower()
        letras = letras.split()

        contagem = Counter(letras)

        for palavra in stopwords:
            contagem.pop(palavra, None)

        lista_palavras = list(contagem.elements())
        
        for palavra in lista_palavras:
            if palavra in musica.lower():
                contador += 1

    except NameError as ne:
        print('NameError. Por favor, digite um valor válido! \n', ne)
    except KeyError as ke:
        print('Não há letra! \n', ke)
    else:
        return f'O número de aparições da temática do título da música {musica} em sua letra é:', contador
