from datetime import datetime
import pandas as pd

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

def create_dataset(k):
    data = None
    for i in range(k):
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

    data.to_csv('final_data.csv')

def create_dataset2(file):
    try:
        new_data = pd.read_csv(file)
        new_data.dropna(inplace=True, subset=['other'])
        create_new_column(new_data['other'], new_data)
        new_data.to_csv(f'new_{file}')
    except AttributeError:
        print(f'Nie powiodło się.')


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
                colname_i = correlation_matrix.columns[i]
                colname_j = correlation_matrix.columns[j]
                highly_correlated_features.add((colname_i, colname_j, correlation_matrix.iloc[i, j]))
    print("Pairs of highly correlated features:")
    for pair in highly_correlated_features:
        print(pair)


def change_genre(x):
    import re
    if re.search('pop', x):
        return 'pop'
    elif re.search('hip hop', x):
        return 'hip hop'
    elif re.search('rock', x):
        return 'rock'
    elif re.search('blues', x):
        return 'blues'
    elif re.search('indie', x):
        return 'indie'
    elif re.search('folk', x):
        return 'folk'
    elif re.search('metal', x):
        return 'metal'
    elif re.search('jazz', x):
        return 'jazz'
    elif re.search('soul', x):
        return 'soul'
    elif re.search('dance', x):
        return 'dance'
    elif re.search('rap', x):
        return 'rap'
    elif re.search('classical', x):
        return 'classical'
    else:
        return 'other'


if __name__ == '__main__':
    create_dataset(24)
