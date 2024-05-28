import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id,
                                                      client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def extract(link, file_path):

    playlist_link = link
    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

    data = pd.DataFrame()
    tracks_names = []
    artist_names = []
    albums = []
    other = []
    art_pop = []
    track_pop_list = []
    track_g = []
    release_date_list = []
    duration_list = []


    for track in sp.playlist_tracks(playlist_URI)["items"]:
        # URI
        track_uri = track["track"]["uri"]

        # Dancebility, energy ...
        other_features = sp.audio_features(track_uri)[0]
        other.append(other_features)

        # Track name
        track_name = track["track"]["name"]
        tracks_names.append(track_name)

        # Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)

        # Name, popularity, genre
        artist_name = track["track"]["artists"][0]["name"]
        artist_names.append(artist_name)
        artist_pop = artist_info["popularity"]
        art_pop.append(artist_pop)
        artist_genres = artist_info["genres"]
        # We can assume the first genre in the list as the main genre of the artist
        artist_genre = artist_genres[0] if artist_genres else None
        track_g.append(artist_genre)

        # Album
        album = track["track"]["album"]["name"]
        albums.append(album)

        # Popularity of the track
        track_pop = track["track"]["popularity"]
        track_pop_list.append(track_pop)

        # Duration - ms
        duration = track["track"]["duration_ms"]
        duration_list.append(duration)

        release_date = track["track"]["album"]["release_date"]
        release_date_list.append(release_date)

    data['track'] = tracks_names
    data['artist'] = artist_names
    data['album'] = albums
    data['other'] = other
    data['artist pop'] = art_pop
    data['track pop'] = track_pop_list
    data['track genre'] = track_g
    data['duration'] = duration_list
    data["release date"] = release_date_list

    data.to_csv(file_path)


def get_playlist_link():

    playlists = []
    with open('playlists.txt', 'r') as f:
        for line in f:
            playlists.append(line)
    return playlists


playlists = get_playlist_link()
for i in range(20, len(playlists)):
    extract(playlists[i], file_path=f'playlist{i}.csv')


