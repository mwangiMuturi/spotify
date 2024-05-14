from main import SpotifyAPI
from requests import post, get
from flask import Flask, render_template, request, redirect, url_for,render_template
import os
client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")

app = Flask(__name__)
api=SpotifyAPI(client_id,client_secret)
token=api.get_token()
artist=api.search_for_artist("Wakadinali")
artist_id=artist["id"]
songs=api.get_songs_by_artist(artist_id)

@app.route('/')
def home():
    return render_template('index.html',songs=songs,artist=artist,counter=0)

@app.route('/search_song/',methods=['GET'])
def index():
    if request.method == "GET":
       
        artist_name = request.args.get('artist')
        # artist_name=request.form['artist']
        artist=api.search_for_artist(artist_name)
        artist_id=artist["id"]
        songs=api.get_songs_by_artist(artist_id)
    
    # for idx,song in enumerate(songs):
    #     output.append(f"{idx+1}.{song["name"]}")
        return render_template ('index.html',songs=songs,artist=artist,counter=0)
    return render_template('index.html',songs=songs,artist=artist,counter=0)



if __name__ == "__main__":
    app.run(debug=True)