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


def read_dataset_fragment(songs_number_from_every_genre: int):
    data = read_dataset()
    list = []
    for g in np.arange(0, 999, 100):
        for i in np.arange(g, g + songs_number_from_every_genre, 1):
            list.append(i)

    data = data.take(list)
    return data
