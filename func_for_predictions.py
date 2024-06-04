import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from yellowbrick.target import FeatureCorrelation
import plotly.express as px

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

    corr_matrix = X.corr()

    fig = px.imshow(corr_matrix, x=feature_names, y=feature_names, color_continuous_scale='gray')
    fig.update_layout(title='Feature Correlation', plot_bgcolor='black', paper_bgcolor='black',
                      font=dict(color='white'), width=800, height=600)
    fig.update_xaxes(tickangle=45, tickfont=dict(color='white'))
    fig.update_yaxes(tickangle=45, tickfont=dict(color='white'))

    st.plotly_chart(fig)


def show_popularity_vs_genre(data):
    fig = px.box(data, x='new genre', y='track pop', title='Popularity of songs by genre',
                 labels={'new genre': 'Genre', 'track pop': 'Song popularity'})

    fig.update_layout(plot_bgcolor='black', paper_bgcolor='black', font=dict(color='white'))

    fig.update_xaxes(tickangle=305)

    st.plotly_chart(fig)

def show_feature_hist(data):
    with plt.style.context('dark_background'):
        plt.figure(figsize=(20, 20))
        data.hist(bins=10, color='skyblue')
        plt.title('Histogram of Features', color='white', pad=20)
        plt.xlabel('Feature Values', color='white', labelpad=20)
        plt.ylabel('Frequency', color='white', labelpad=20)
        plt.xticks(color='white', fontsize=9)
        plt.yticks(color='white', fontsize=9)
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.tight_layout()
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()