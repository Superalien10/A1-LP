from analise_palavras import *


print(analise_discografia('Álbum'))

print(analise_discografia('Música'))

print(analise_discografia('Letra'))

nuvem_palavras('Álbum')

nuvem_palavras('Música')

nuvem_palavras('Letra')


albuns_discografia = df_seu_jorge['Álbum'].unique()

for albuns in albuns_discografia:
    print(palavras_musicas_album(albuns))
    print(recorrencia_album_letra(albuns))
    print('\n')


musicas_discografia = df_seu_jorge['Música'].unique()

for musicas in musicas_discografia:
        print(recorrencia_musica_letra(musicas), '\n')

print(recorrencia_musica_letra('Saravá'))

