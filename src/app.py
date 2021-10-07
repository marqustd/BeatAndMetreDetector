import logging
import os
import pandas
from tempometredetector import tempo_metre_detector
from tempometredetector.metredetector.spectrogram.spectrogram_metre_detector import (
    SpectrogramMetreDetector,
)


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


def test_data_songs():
    detector = tempo_metre_detector.TempoMetreDetector(
        tempo_detector=None, metre_detector=SpectrogramMetreDetector
    )

    data = read_dataset_only_metre()
    good = 0
    bad = 0
    all_songs = len(data)
    for song in data.iloc:
        path = song.path
        path = os.path.relpath("../dataset/genres" + path)
        song.path = path

        result_tempo, result_metre, time = detector.detect(
            song.tempo, song.metre, song.path
        )

        expectedMetre = int(song.metre.split("/")[0])

        if result_metre == expectedMetre or (
            expectedMetre == 4 and (result_metre == 2 or result_metre == 8)
        ):
            print(f"Good detection! {expectedMetre} - {song.path}")
            good += 1
        else:
            print(f"Exptected {expectedMetre} but detect {result_metre} - {song.path}")
            bad += 1

    print(f"All: {all_songs}")
    print(f"Good: {good}")
    print(f"Bad: {bad}")
    print(f"Accuracy: {good/all_songs}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    test_data_songs()
