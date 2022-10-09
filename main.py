from analise_palavras import *
import busca_spotify as spo
import busca_discografia as disco
import criar_df as cdf
import respondendo/analise as an

print("DataFrame principal")
cdf.criar_tabela()
print("DataFrames subjacentes")
an.criar_album_vis()
an.criar_album_dur()
an.criar_musica_vis()
an.criar_musica_dur()
an.criar_album_pre()
an.criar_album_pop()
an.criar_musica_pop()


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



