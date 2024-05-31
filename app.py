import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
import pickle
from yellowbrick.target import FeatureCorrelation
import numpy as np
import matplotlib.pyplot as plt

def get_popularity(data, artist):
    filt = data['artist'] == artist
    return data[filt]['artist pop'].iloc[0]

def synchronize_columns(df1, df2):
    column_order = df2.columns.tolist()
    missing_in_df1 = set(df2.columns) - set(df1.columns)
    for col in missing_in_df1:
        df1[col] = 0
    df1 = df1[column_order]

    return df1, df2

def show_correlation(data):
    feature_names = ['acousticness', 'danceability', 'energy', 'instrumentalness',
                     'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'duration', 'year']

    X, y = data[feature_names], data['track pop']

    features = np.array(feature_names)

    visualizer = FeatureCorrelation(labels=features)

    plt.rcParams['figure.figsize'] = (10, 8)
    visualizer.fit(X, y)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

def show_feature_hist(data):
    data.hist(figsize=(15, 12), bins=10)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

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

    if st.button("Show feature distirbutions"):
        show_feature_hist(data)

    frame = inputs(data)

    if st.button('Predykcja'):
        st.write(predict_pop(en_data, frame))


if __name__ == '__main__':
    main()

