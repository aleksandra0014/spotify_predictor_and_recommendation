import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
def show_track_per_year(data):
    tracks_by_year = data.groupby('year').size().reset_index(name='count')
    plt.style.use('ggplot')
    tracks_by_year.plot(x='year', y='count', legend=None, color='pink')
    plt.xlabel('Year')
    plt.ylabel('Number of tracks')
    plt.title('Number of tracks by year')
    st.pyplot()

def show_pop_artist(data):
    df = data[['artist pop', 'artist']].sort_values(by='artist pop', ascending=False).drop_duplicates(
        subset=['artist']).head(10)
    st.dataframe(df)

def show_pop_tracks(data):
    df = data[['track pop', 'track', 'artist']].sort_values(by='track pop', ascending=False).drop_duplicates().head(10)
    st.dataframe(df)


def show_genre(data):
    number_genre = data.groupby('new genre').size().reset_index(name='count')
    number_genre = number_genre.sort_values(by='count', ascending=False)
    colors = plt.cm.get_cmap('RdBu', len(number_genre))
    plt.bar(number_genre['new genre'], number_genre['count'], color=colors(range(len(number_genre))))
    plt.xlabel('Genre')
    plt.ylabel('Number of tracks')
    plt.title('Number of tracks per genre')
    plt.xticks(rotation=45)
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()


def show_pop_density(data):
    sns.histplot(x='track pop', data=data, bins=25, kde=True, color='skyblue')
    plt.title('Popularity density')
    plt.xlabel('Track popularity')
    plt.ylabel('Frequency')
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()