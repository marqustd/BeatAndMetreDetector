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
    data = data[:1000]  # todo remove
    data = data[data.metre.notnull()]
    return data


def check_metre_accuracy_1(song, result_metre, expected_metre):
    if result_metre == expected_metre:
        print(f"Good detection! {expected_metre} - {song.path}")
        return True


def check_metre_accuracy_2(song, result_metre, expected_metre, denumerator):
    if denumerator == 8 and expected_metre % 2 == 0:
        expected_metre = expected_metre / 2

    if denumerator == 2:
        expected_metre = expected_metre * 2

    if result_metre == expected_metre:
        print(f"Good detection2! {expected_metre} - {song.path}")
        return True


def register_bad_metre_detection(
    song, result_metre, expected_metre_numerator, denumerator
):
    print(
        f"Exptected {expected_metre_numerator}/{denumerator} but detect {result_metre} - {song.path}"
    )


def test_data_songs():
    detector = tempo_metre_detector.TempoMetreDetector(
        tempo_detector=None, metre_detector=SpectrogramMetreDetector
    )

    data = read_dataset_only_metre()
    good1 = 0
    good2 = 0
    bad = 0
    all_songs = len(data)
    for song in data.iloc:
        path = song.path
        path = os.path.relpath("../dataset/genres" + path)
        song.path = path

        result_tempo, result_metre, time = detector.detect(
            song.tempo, song.metre, song.path
        )

        expected_metre_numerator, denumerator = song.metre.split("/")
        expected_metre_numerator = int(expected_metre_numerator)
        denumerator = int(denumerator)

        if check_metre_accuracy_1(song, result_metre, expected_metre_numerator):
            good1 += 1
            good2 += 1
        elif check_metre_accuracy_2(
            song, result_metre, expected_metre_numerator, denumerator
        ):
            good2 += 1
        else:
            register_bad_metre_detection(
                song, result_metre, expected_metre_numerator, denumerator
            )
            bad += 1

    print(f"All: {all_songs}")
    print(f"Good1: {good1}")
    print(f"Good2: {good2}")
    print(f"Bad: {bad}")
    print(f"Metre accuracy1: {good1/all_songs}")
    print(f"Metre accuracy2: {good2/all_songs}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_data_songs()
