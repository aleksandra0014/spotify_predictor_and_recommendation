import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from yellowbrick.target import FeatureCorrelation


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

def show_popularity_vs_genre(data):
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='new genre', y='track pop', data=data, palette='Reds')
    plt.title('Rozkład popularności piosenek według gatunku')
    plt.xlabel('Gatunek')
    plt.ylabel('Popularność piosenki')
    plt.xticks(rotation=305)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()

def show_feature_hist(data):
    data.hist(figsize=(15, 12), bins=10)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()