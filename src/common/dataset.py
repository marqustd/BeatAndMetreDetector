import numpy as np
import pandas


def read_dataset():
    data = pandas.read_csv(
        "../dataset/genres/genres_tempos.csv",
        sep=",",
        names=["path", "tempo", "metre"],
    )
    return data


def read_dataset_only_metre():
    data = read_dataset()
    data = data[data.metre.notnull()]
    return data


def read_dataset_genres_fragment(songs_number_from_every_genre: int):
    genres = read_dataset_genres()
    list = []
    for g in np.arange(0, 999, 100):
        for i in np.arange(g, g + songs_number_from_every_genre, 1):
            list.append(i)

    genres = genres.take(list)
    return genres


def read_dataset_genres():
    data = read_dataset()
    return data[:1000]
