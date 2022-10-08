import requests
import datetime
from urllib.parse import urlencode
import base64

client_id = '14e7ee36b83c49328699223fb71e4821'
client_secret = 'f19bdf678fe846939e46368c8ff19e8f'

class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"
    
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()
    
    def get_token_headers(self):
        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"
        }
    
    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        } 
    
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in'] # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True
    
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token() 
        return token
    
    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()
    
    def get_album(self, _id):
        return self.get_resource(_id, resource_type='albums')
    
    def get_artist(self, _id):
        return self.get_resource(_id, resource_type='artists')
    
    def base_search(self, query_params): # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):  
            return {}
        return r.json()
    
    def search(self, query=None, operator=None, operator_query=None, search_type='artist' ):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)

spotify = SpotifyAPI(client_id, client_secret)

result = spotify.search(query="Beds are burning", search_type="track")


"""
print(type(result))
for a in result:
    print(a,":",result[a])
    tracks=result[a]
print(type(tracks))
for a in tracks:
    print(a,":", tracks[a])
print(type(tracks["items"]))
items = tracks["items"]
exemplo = items[0]
for key in exemplo:
    print(key,":", exemplo[key], "###\n\n\n")"""
"""
#Pegando a popularidade e a duração de uma música:
musica = "Beds are burning"
tracks = spotify.search(query=musica, search_type="track")["tracks"]
popularidade = tracks["items"][0]["popularity"]
duracao = tracks["items"][0]["duration_ms"]
print(popularidade, duracao)

"""


""" Versão anterior
print(type(result))
print("Resultado: \n", result)
for key in result:
    print("Chave: \n", key)
    tracks = result[key]
    print("Conteúdo: \n", result[key])
    for track in tracks:
        print("Track: \n", track)
        print("Valor: \n", tracks[track])
        if type(track)==dict:
            for chave in track:
                print("Chave de track: \n", chave)
                print("Conteúdo de chave de track: \n", track[chave])
        print(type(track))
        print(type(tracks[track]))
    #item=dict(tracks["items"])
    for item in tracks["items"]:
        print(item, "\n\n\n")
        print(type(item))
        print("#"*10)
        for chave in item:
            print(chave, ":", item[chave])
            if chave["name"]=="The Souljazz Orchestra":
                print(chave, ":", item[chave])

            ou if tracks["artists"]["names"]?
"""
"""
print(type(result))
print("Resultado: \n", result)
for tipo in result:
    result[tipo]
    print("Conteúdo: \n", result[tipo])
    for secao in result[tipo]:
        print("Seção: \n", secao)
        print("Valor: \n", result[tipo][secao])
    for elemento in result[tipo]["items"]:
        print("Item da lista: \n", elemento)
        print("#"*10)
        for chave in elemento:
            print(chave, ":", elemento[chave])
            print(type(elemento))
            print(type(elemento[chave]))
            
            type(elemento[chave][0]["artists"])
            type(elemento)
            x=elemento[chave]["artists"][0]
            print("\n\n\n", x["name"], "\n\n\n")
            if x["name"]=="The Souljazz Orchestra":
                print(chave, ":", elemento[chave])"""
"""
nomes = []
print(type(result))
print("Resultado: \n", result)
for tipo in result:
    result[tipo]
    print("Conteúdo: \n", result[tipo])
    for secao in result[tipo]:
        print("Seção: \n", secao)
        print("Valor: \n", result[tipo][secao])
    for elemento in result[tipo]["items"]:
        print("Item da lista: \n", elemento)
        print("#"*10)
        for chave in elemento:
            print(chave, ":", elemento[chave])
        print(" \n"*5)
        print(elemento["artists"][0]["name"])
        nomes.append(elemento["artists"][0]["name"])
print("\n\n\n\n\n", nomes)

"""



print("end")
