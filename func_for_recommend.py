from extracting_data import extract
from utilis import change_date, change_genre
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

def synchronize(df1, df2):
    missing_in_df2 = set(df1.columns) - set(df2.columns)
    missing_in_df1 = set(df2.columns) - set(df1.columns)

    for col in missing_in_df2:
        df2[col] = 0

    for col in missing_in_df1:
        df1[col] = 0

    df1 = df1[sorted(df1.columns)]
    df2 = df2[sorted(df2.columns)]

    return df1, df2

def scale_data(data, column_names):
    df = pd.DataFrame(data, columns=column_names)
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df)
    scaled_df = pd.DataFrame(scaled_data, columns=column_names)
    return scaled_df

def change_string(x):
    x = x.replace('{', '')
    x = x.replace('}', '')
    x = x.split(',')
    return x


def tranform_column(column):
    d = column.apply(change_string)
    list_of_dictionaries = []
    for row in d:
        data_dict = {}
        for item in row:
            item = item.replace("'", "").strip()
            key, value = item.split(':', 1)
            data_dict[key.strip()] = value.strip()
        list_of_dictionaries.append(data_dict)

    return list_of_dictionaries


def create_new_column(column, df):
    l = tranform_column(column)

    danceability = []
    energy = []
    loudness = []
    speechiness = []
    acousticness = []
    instrumentalness = []
    liveness = []
    valence = []
    tempo = []

    for dic in l:
        danceability.append(dic['danceability'])
        energy.append(dic['energy'])
        loudness.append(dic['loudness'])
        speechiness.append(dic['speechiness'])
        acousticness.append(dic['acousticness'])
        instrumentalness.append(dic['instrumentalness'])
        liveness.append(dic['liveness'])
        valence.append(dic['valence'])
        tempo.append(dic['tempo'])

    df['danceability'] = danceability
    df['energy'] = energy
    df['loudness'] = loudness
    df['speechiness'] = speechiness
    df['acousticness'] = acousticness
    df['instrumentalness'] = instrumentalness
    df['liveness'] = liveness
    df['valence'] = valence
    df['tempo'] = tempo

    df.drop(columns=['other'], inplace=True)

    return df

def get_playlist_data(link, file_name):
    extract(link, f'{file_name}.csv')
    new_data = pd.read_csv(f'{file_name}.csv')
    new_data.dropna(inplace=True, subset=['other'])
    create_new_column(new_data['other'], new_data)
    new_data.drop([new_data.columns[0]], axis=1, inplace=True)
    new_data['year'] = new_data['release date'].apply(change_date)
    new_data.drop(columns='release date', inplace=True)
    new_data['track genre'].fillna('Inne', inplace=True)
    new_data['new genre'] = new_data['track genre'].apply(change_genre)
    new_data.drop(columns='track genre', inplace=True)
    encoded_data = pd.get_dummies(new_data, columns=['new genre'], drop_first=True, dtype=int)
    return encoded_data, new_data


def recomend(playlist_encoded, playlist):
    playlist_num = playlist_encoded.drop(columns=['artist', 'album', 'track'])
    scaled_playlist = scale_data(data=playlist_num, column_names=playlist_num.columns)
    spotify_data = pd.read_csv('spotify_data_encoded2.csv')
    spotify_data.drop([spotify_data.columns[0]], axis=1, inplace=True)
    spotify_data_num = spotify_data.drop(columns=['track', 'artist', 'album'])
    spotify_data_scaled = scale_data(spotify_data_num, spotify_data_num.columns)

    column_averages = scaled_playlist.mean()
    averages_cosine_sim = pd.DataFrame([column_averages], index=['Average'])
    synchronize(spotify_data_scaled, averages_cosine_sim)
    averages_cosine_sim = averages_cosine_sim.sort_index(axis=1)
    spotify_data_scaled = spotify_data_scaled.sort_index(axis=1)

    similarity_scores = cosine_similarity(spotify_data_scaled, averages_cosine_sim)
    spotify_data['similarity_score'] = similarity_scores

    new_frame = pd.merge(spotify_data, playlist, how='left', on='track')
    top_similarities_filtered = new_frame[new_frame.isna().any(axis=1)]
    top_similarities_filtered = top_similarities_filtered.sort_values(by='similarity_score', ascending=False)
    top_similarities_filtered = top_similarities_filtered.drop_duplicates(subset=['track', 'artist_x'])
    return top_similarities_filtered
