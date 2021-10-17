import logging
import os
import pandas
from tempometredetector import tempo_metre_detector
from tempometredetector.metredetector.spectrogram.spectrogram_metre_detector import (
    SpectrogramMetreDetector,
)
from tempometredetector.tempodetector.comb_filter_tempo_detector import (
    CombFilterTempoDetector,
)


def read_dataset():
    data = pandas.read_csv(
        "../dataset/genres/genres_tempos.csv",
        sep=",",
        names=["path", "tempo", "metre"],
    )
    return data[:100]


def read_dataset_only_metre():
    data = read_dataset()
    # data = data[1000:]  # todo remove
    data = data[data.metre.notnull()]
    return data


def check_metre_accuracy_1(song, result_metre, expected_metre):
    if result_metre == expected_metre:
        print(f"Good metre detection - acc1! {expected_metre} - {song.path}")
        return True
    return False


def check_metre_accuracy_2(song, result_metre, expected_metre, denumerator):
    if denumerator == 8 and expected_metre % 2 == 0:
        expected_metre = expected_metre / 2

    if result_metre == expected_metre or result_metre == 2 * expected_metre:
        print(f"Good metre detection - acc2! {expected_metre} - {song.path}")
        return True
    return False


def register_bad_metre_detection(
    song, result_metre, expected_metre_numerator, denumerator
):
    print(
        f"Exptected {expected_metre_numerator}/{denumerator} but detect {result_metre} - {song.path}"
    )
    return False


def test_data_songs_metre():
    detector = tempo_metre_detector.TempoMetreDetector(
        tempo_detector=None, metre_detector=SpectrogramMetreDetector
    )

    good_metre_acc1 = 0
    good_metre_acc2 = 0
    bad_metre = 0

    data = read_dataset_only_metre()
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
            good_metre_acc1 += 1
            good_metre_acc2 += 1
        elif check_metre_accuracy_2(
            song, result_metre, expected_metre_numerator, denumerator
        ):
            good_metre_acc2 += 1
        else:
            register_bad_metre_detection(
                song, result_metre, expected_metre_numerator, denumerator
            )
            bad_metre += 1

    print(f"All: {all_songs}")
    print(f"Good metre - accuracy1: {good_metre_acc1}")
    print(f"Good metre - accuracy2: {good_metre_acc2}")
    print(f"Bad: {bad_metre}")
    print(f"Metre accuracy1: {good_metre_acc1/all_songs}")
    print(f"Metre accuracy2: {good_metre_acc2/all_songs}")


def test_data_songs_tempo():
    detector = tempo_metre_detector.TempoMetreDetector(
        tempo_detector=CombFilterTempoDetector, metre_detector=None
    )

    good_tempo_acc1 = 0
    good_tempo_acc2 = 0
    bad_tempo = 0

    data = read_dataset()

    all_songs = len(data)
    for song in data.iloc:
        path = song.path
        path = os.path.relpath("../dataset/genres" + path)
        song.path = path

        result_tempo, result_metre, time = detector.detect(
            song.tempo, song.metre, song.path
        )

        expected_tempo = song.tempo

        if expected_tempo == result_tempo:
            logging.info(f"Good tempo detection - acc1! {expected_tempo} - {song.path}")
            good_tempo_acc1 += 1
            good_tempo_acc2 += 1
        elif expected_tempo == 2 * result_tempo or expected_tempo == 0.5 * result_tempo:
            logging.info(f"Good tempo detection - acc2! {expected_tempo} - {song.path}")
            good_tempo_acc2 += 1
        else:
            logging.info(
                f"Exptected {expected_tempo} but detect {result_tempo} - {song.path}"
            )
            bad_tempo += 1

    print(f"All: {all_songs}")
    print(f"Good tempo - accuracy1: {good_tempo_acc1}")
    print(f"Good tempo - accuracy2: {good_tempo_acc2}")
    print(f"Bad: {bad_tempo}")
    print(f"Tempo accuracy1: {good_tempo_acc1/all_songs}")
    print(f"Tempo accuracy2: {good_tempo_acc2/all_songs}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # test_data_songs_metre()
    test_data_songs_tempo()
