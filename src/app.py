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
    y = st.text_input('Year:', value='2024')
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
    st.sidebar.title('🎶'
                     'Welcome in Spotify'
                     '🎶')
    st.sidebar.subheader('Select what you want to do👇️')
    # Opcje w bocznym menu
    option = st.sidebar.selectbox(
        'Your options:',
        ['Prediction', 'Recommender']
    )
    if option == 'Prediction':

        data = pd.read_csv('dane_po_EDA.csv')
        en_data = pd.read_csv('spotify_data_encoded2.csv')
        en_data.drop([en_data.columns[0]], axis=1, inplace=True)
        en_data.drop(columns=['track', 'album', 'artist', 'instrumentalness', 'acousticness', 'track pop'], inplace=True)
        data.drop([data.columns[0]], axis=1, inplace=True)


        st.title("🔮 Spotify Popularity Predictions")
        if st.button('Show data base'):
            st.write(data)

        if st.button("Show correaltion with target"):
            show_correlation(data)

        if st.button("Show popularity by genre"):
            show_popularity_vs_genre(data)

        if st.button("Show feature distirbutions"):
            show_feature_hist(data)

        st.markdown('### Predict popularity of your song!🔍')
        frame = inputs(data)
        if st.button('Prediction', type="primary"):
            st.write(
                """
                <style>
                .centered-row {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    flex-direction: column;
                    text-align: center;
                }
                .green-text {
                    color: green; /* Zielony kolor tekstu */
                    font-size: 36px; /* Powiększenie tekstu */
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="centered-row">
                    <p>Predicted Popularity</p>
                    <p class="green-text">{}</p>
                </div>
                """.format(round(predict_pop(en_data, frame)[0],2)),
                unsafe_allow_html=True
            )

            show_pop_density(data, round(predict_pop(en_data, frame)[0],2), True)
    else:
        st.title("🎧 Spotify Song Recommender")
        link = st.text_input('Link:',
                             value='https://open.spotify.com/playlist/041EEjr8FMkWlzbuKnSXYD?si=161e174cef984d55')

        if 'previous_link' not in st.session_state:
            st.session_state['previous_link'] = ''

        if 'playlist_data' not in st.session_state:
            st.session_state['playlist_data'] = None

        if 'playlist_encoded' not in st.session_state:
            st.session_state['playlist_encoded'] = None

        # Check if the link has changed
        if link != st.session_state['previous_link']:
            st.session_state['previous_link'] = link
            playlist_encoded, playlist = get_playlist_data(link, 'p')
            st.session_state['playlist_encoded'] = playlist_encoded
            st.session_state['playlist_data'] = playlist
        else:
            playlist_encoded = st.session_state['playlist_encoded']
            playlist = st.session_state['playlist_data']

        if st.button("Check your playlist analysis"):
            st.subheader("Your playlist")
            st.dataframe(playlist)
            st.subheader("10 the most popular artist from playlist")
            show_pop_artist(playlist)
            st.subheader("10 the most popular tracks from playlist")
            show_pop_tracks(playlist)
            st.subheader("Genre in playlist")
            show_genre(playlist)
            st.subheader("Amount of tracks from each year")
            show_track_per_year(playlist)
            st.subheader("Track popularity density")
            show_pop_density(playlist, 0)

        st.subheader("Check your playlist recommendations")
        top_similarities_filtered = recomend(playlist_encoded, playlist)
        n = st.slider('Number of tracks:', min_value=1, max_value=50, value=20)
        if st.button('Check', type='primary'):
            top_similarities_filtered_display = top_similarities_filtered[
                ['track', 'artist_x', 'similarity_score']].head(n).reset_index(drop=True)
            st.dataframe(top_similarities_filtered_display)



if __name__ == '__main__':
    main()

