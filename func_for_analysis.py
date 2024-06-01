import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
def show_track_per_year(data):
    tracks_by_year = data.groupby('year').size().reset_index(name='count')
    plt.style.use('ggplot')
    tracks_by_year.plot(x='year', y='count', legend=None)
    plt.xlabel('year')
    plt.ylabel('number of tracks')
    plt.title('Number of tracks by year')
    st.pyplot()

def show_pop_artist(data):
    data[['artist pop', 'artist']].sort_values(by='artist pop', ascending=False).drop_duplicates(
        subset=['artist']).head(10)

def show_pop_tracks(data):
    data[['track pop', 'track', 'artist']].sort_values(by='track pop', ascending=False).drop_duplicates().head(10)

def show_genre(data):
    number_genre = data.groupby('new genre').size().reset_index(name='count')
    number_genre.sort_values(by='count', ascending=False)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    plt.bar(number_genre['new genre'], number_genre['count'], color=colors)
    plt.xlabel('Gatunek')
    plt.ylabel('Liczba utworów')
    plt.title('Liczba utworów w poszczególnych gatunkach')
    plt.xticks(rotation=45)
    st.pyplot()

def show_pop_density(data):
    sns.histplot(x='track pop', data=data, bins=25, kde=True, color='skyblue')
    plt.title('Różnorodność naszego targetu')
    plt.xlabel('Popularność piosenek')
    plt.ylabel('Częstotliwość')