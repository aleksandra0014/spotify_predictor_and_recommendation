import streamlit as st
from sklearn.preprocessing import StandardScaler
import pickle
from yellowbrick.target import FeatureCorrelation
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from extracting_data import extract
from utilis import change_date, change_genre
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from func_for_analysis import *
from func_for_recommend import *
from func_for_predictions import *

def inputs(data):
    description = data.describe()
    des = description.loc[['min', 'max', 'mean']]

    artist_input = st.text_input('Wpisz nazwę artysty:')
    try:
        pop = get_popularity(data, artist_input)
        pop = int(pop)
    except:
        pop = 0

    st.write(des['duration'])
    duration_input = st.number_input('Wpisz długość trwania piosenki (ms):')
    st.write(des['energy'])
    e = st.number_input('Energy:')
    st.write(des['danceability'])
    d = st.number_input('Danceability: ')
    st.write(des['loudness'])
    l = st.number_input('Loudness:')
    st.write(des['speechiness'])
    s = st.number_input('Speechiness:')
    st.write(des['tempo'])
    t = st.number_input('Tempo:')
    st.write(des['liveness'])
    li = st.number_input('Liveness:')
    st.write(des['valence'])
    v = st.number_input('Valence:')
    y = st.text_input('Year:', value='2020')
    y = int(y)
    g = st.selectbox('Genre:',
                     ['pop', 'hip hop', 'classical', 'dance', 'folk', 'soul', 'rock', 'metal', 'rap', 'jazz', 'indie',
                      'other'])
    frame = pd.DataFrame(
        {'artist pop': [pop], 'duration': [duration_input], 'danceability': [d], 'energy': [e], 'loudness': [l],
         'speechiness': [s], 'liveness': [li], 'valence': [v], 'tempo': [t], 'year': [y], 'new genre': [g]},
        index=[0])
    return frame

def predict_pop(en_data, row):
    encoded_frame = pd.get_dummies(row, columns=['new genre'], dtype=int)
    synchronize_columns(encoded_frame, en_data)
    with open('rf_model.pkl', 'rb') as f:
        model = pickle.load(f)
    pred = model.predict(encoded_frame)
    return pred


def main():
    # Dodawanie elementów do bocznego menu
    st.sidebar.title('Boczne Menu')

    # Opcje w bocznym menu
    option = st.sidebar.selectbox(
        'Wybierz funkcjonalność:',
        ['Prediction', 'Recommender']
    )
    if option == 'Prediction':

        data = pd.read_csv('dane_po_EDA.csv')
        en_data = pd.read_csv('spotify_data_encoded2.csv')
        en_data.drop([en_data.columns[0]], axis=1, inplace=True)
        en_data.drop(columns=['track', 'album', 'artist', 'instrumentalness', 'acousticness', 'track pop'], inplace=True)
        data.drop([data.columns[0]], axis=1, inplace=True)

        st.title("Spotify predictions")
        if st.button('Show data base'):
            st.write(data)

        if st.button("Show correaltion with target"):
            show_correlation(data)

        if st.button("Show popularity by genre"):
            show_popularity_vs_genre(data)

        if st.button("Show feature distirbutions"):
            show_feature_hist(data)

        frame = inputs(data)

        if st.button('Prediction', type="primary"):
            st.write(predict_pop(en_data, frame))
    else:
        st.title("Spotify recommend system")
        link = st.text_input('Link:', value='https://open.spotify.com/playlist/041EEjr8FMkWlzbuKnSXYD?si=161e174cef984d55')
        playlist_encoded, playlist = get_playlist_data(link, 'p')
        if st.button("Check your playlist analysis"):
            if st.button("Show you playlist"):
                st.dataframe(playlist)
            if st.button("Show 10 the most popular artist from playlist"):
                show_pop_artist(playlist)
            if st.button("Show 10 the most popular tracks from playlist"):
                show_pop_tracks(playlist)
            if st.button("Show genre in playlist"):
                show_genre(playlist)
            if st.button("Show amount of tracks from each year"):
                show_track_per_year(playlist)
            if st.button("Show track popularity density"):
                show_pop_density(playlist)

        if st.button("Check your playlist recommendations"):
            top_similarities_filtered = recomend(playlist_encoded, playlist)
            n = st.slider('Number of tracks:', min_value=1, max_value=50, value=20)
            top_similarities_filtered_display = top_similarities_filtered[
                ['track', 'artist_x', 'similarity_score']].head(n).reset_index(drop=True)
            st.dataframe(top_similarities_filtered_display)


if __name__ == '__main__':
    main()

