from dotenv import load_dotenv
import base64
import json
load_dotenv()   
import os
from requests import get,post

client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")
class SpotifyAPI:
    def __init__(self,client_id,client_secret):
        self.client_id=client_id
        self.client_secret=client_secret
        self.token=self.get_token()
    
    def get_token(self):
        auth_string=self.client_id+":"+self.client_secret
        auth_bytes=auth_string.encode('utf-8')
        auth_base64=str(base64.b64encode(auth_bytes),'utf-8')

        url="https://accounts.spotify.com/api/token"
        headers={
            "Authorization":"Basic "+auth_base64,
            "content-type":"application/x-www-form-urlencoded"
        }
        data={"grant_type":"client_credentials"}

        result=post(url,headers=headers,data=data)
        json_result=json.loads(result.content)
        token=json_result['access_token']
        return token

    def get_auth_header(self):
        return {"authorization":"Bearer "+self.token}

    def search_for_artist(self,artist_name):
        url="https://api.spotify.com/v1/search"
        headers=self.get_auth_header()
        query=f"?q={artist_name}&type=artist&limit=1"
        query_url=url+query
        result=get(query_url,headers=headers)
        json_result=json.loads(result.content)["artists"]["items"]
        if len(json_result)==0:
            print("No artist with this name exists...")
            return None
        return json_result[0]

    def get_songs_by_artist(self,artist_id):
        url=f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
        headers=self.get_auth_header()
        query="?market=US"
        query_url=url+query
        result=get(query_url,headers=headers)
        json_result=json.loads(result.content)["tracks"]
        return json_result
api=SpotifyAPI(client_id,client_secret)
token=api.get_token()
artist=api.search_for_artist("SZA")
artist_id=artist["id"]
songs=api.get_songs_by_artist(artist_id)
# for idx,song in enumerate(songs):
#     print(f"{idx+1}.{song["name"]}")
# print (artist["name"],[artist["genres"]])
# print(token)


