from datetime import datetime


def change_string(x):
    x = x.replace('{', '')
    x = x.replace('}', '')
    x = x.split(',')
    return x


def tranform_column(column):
    d = column.apply(change_string)
    list_of_dictionaries = []
    data_dict = {}
    for row in d:
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

def create_dataset():
    data = None
    for i in range(24):
        print(i)
        try:
            new_data = pd.read_csv(f'playlist{i}.csv')
            new_data.dropna(inplace=True, subset=['other'])
            create_new_column(new_data['other'], new_data)
            if data is None:
                data = new_data
            else:
                data = pd.concat([data, new_data])
        except AttributeError:
            print(f'Nie powiodło się z {i}')

    data.to_csv('spotify_data.csv')


def change_date(x):
    try:
        date_object = datetime.strptime(x, '%Y-%m-%d')
        return date_object.year
    except ValueError:
        try:
            date_object = datetime.strptime(x, '%Y')
            return date_object.year
        except ValueError:
            try:
                date_object = datetime.strptime(x, '%Y-%m')
                return date_object.year
            except ValueError:
                print('Nieznany format')


def cor_features(df):
    highly_correlated_features = set()
    correlation_matrix = df.corr().abs()
    for i in range(len(correlation_matrix.columns)):
        for j in range(i):
            if correlation_matrix.iloc[i, j] > 0.6:
                colname = correlation_matrix.columns[i]
                highly_correlated_features.add(colname)
    print("Highly correlated features:", highly_correlated_features)


def signif_features(df):
    significant_features = df.corr()['stroke'].abs().sort_values(ascending=False)
    significant_features = significant_features[significant_features > 0.1].index.tolist()
    for i in significant_features:
        print(i)
    return significant_features


if __name__ == '__main__':
    import pandas as pd
    from datetime import datetime
    create_dataset()