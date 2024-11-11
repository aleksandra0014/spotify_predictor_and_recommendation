import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def show_track_per_year(data):
    tracks_by_year = data.groupby('year').size().reset_index(name='count')
    fig = px.line(tracks_by_year, x='year', y='count', title='Number of tracks by year',
                  labels={'year': 'Year', 'count': 'Number of tracks'},
                  template='plotly_dark', line_shape='spline')
    fig.update_traces(line=dict(color='pink'))
    st.plotly_chart(fig)

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
    fig = px.bar(number_genre, x='new genre', y='count', color='count',
                 labels={'new genre': 'Genre', 'count': 'Number of tracks'},
                 title='Number of tracks per genre', template='plotly_dark')
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)


def show_pop_density(data, x, add_x=False):
    fig = px.histogram(data, x='track pop', nbins=25, histnorm='density', color_discrete_sequence=['skyblue'])
    fig.update_layout(title='Popularity density', plot_bgcolor='black', paper_bgcolor='black',
                      font=dict(color='white'), xaxis=dict(title='Track popularity', color='white'),
                      yaxis=dict(title='Frequency', color='white'), width=800, height=600)
    fig.update_traces(marker=dict(line=dict(color='black', width=0.5)))
    if add_x:
        fig.add_vline(x=x, line=dict(color='red', width=1, dash='dash'), annotation_text=f'fValue: {x}',
                      annotation_position="top left")
    st.plotly_chart(fig)
