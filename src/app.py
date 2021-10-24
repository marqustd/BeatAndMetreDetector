import time
import logging
import os
from common.accuraccy_data import AccuraccyData
from common.logger import config_logger
from common.dataset import *
from common.tempo import *
from common.metre import *
import settings
import pandas
from tempometredetector import tempo_metre_detector
from tempometredetector.metredetector.base_metre_detector import BaseMetreDetector
from tempometredetector.metredetector.spectrogram.spectrogram_metre_detector import (
    SpectrogramMetreDetector,
)
from tempometredetector.tempodetector.base_tempo_detector import BaseTempoDetector
from tempometredetector.tempodetector.comb_filter_tempo_detector import (
    CombFilterTempoDetector,
)
from tempometredetector.tempodetector.convolve_tempo_detector import (
    ConvolveTempoDetector,
)


def write_settings():
    for property, value in vars(settings).items():
        logging.info(f"{property} : {value}")


def test_data_songs_metre(metre_detector: BaseMetreDetector):
    config_logger(f"metre-{metre_detector()}.log")

    detector = tempo_metre_detector.TempoMetreDetector(
        tempo_detector=None, metre_detector=metre_detector
    )

    startTime = time.time()
    acc_data = AccuraccyData()

    data = read_dataset_only_metre()
    all_songs = len(data)
    for song in data.iloc:
        path = song.path
        path = os.path.relpath("../dataset/genres" + path)
        song.path = path

        result_tempo, result_metre, _ = detector.detect(
            song.tempo, song.metre, song.path
        )

        expected_metre_numerator, denumerator = song.metre.split("/")
        expected_metre_numerator = int(expected_metre_numerator)
        denumerator = int(denumerator)

        check_metre_detection(
            acc_data, song, result_metre, expected_metre_numerator, denumerator
        )

    summarize_metre_detection(metre_detector, acc_data, all_songs)
    totalTime = time.time() - startTime
    logging.info(f"Total time: {totalTime}")


def test_data_songs_tempo(tempo_detector: BaseTempoDetector):
    config_logger(f"tempo-{tempo_detector()}.log")

    detector = tempo_metre_detector.TempoMetreDetector(
        tempo_detector=tempo_detector, metre_detector=None
    )

    startTime = time.time()
    acc_data = AccuraccyData()
    data = read_dataset_fragment(10)

    all_songs = len(data)
    for song in data.iloc:
        path = song.path
        path = os.path.relpath("../dataset/genres" + path)
        song.path = path

        result_tempo, result_metre, _ = detector.detect(
            song.tempo, song.metre, song.path
        )

        expected_tempo = song.tempo

        check_tempo_detection(acc_data, song, result_tempo, expected_tempo)

    summarize_tempo_detection(tempo_detector, acc_data, all_songs)
    totalTime = time.time() - startTime
    logging.info(f"Total time: {totalTime}")


def test_data_songs(
    tempo_detector: BaseTempoDetector, metre_detector: BaseMetreDetector
):
    config_logger(f"tempo-{tempo_detector()}_metre-{metre_detector()}.log")

    detector = tempo_metre_detector.TempoMetreDetector(
        tempo_detector=tempo_detector, metre_detector=metre_detector
    )

    startTime = time.time()
    tempo_acc_data = AccuraccyData()
    metre_acc_data = AccuraccyData()
    data = read_dataset_only_metre()

    all_songs = len(data)
    for song in data.iloc:
        path = song.path
        path = os.path.relpath("../dataset/genres" + path)
        song.path = path

        result_tempo, result_metre, time = detector.detect(
            song.tempo, song.metre, song.path
        )

        expected_tempo = song.tempo
        check_tempo_detection(tempo_acc_data, song, result_tempo, expected_tempo)

        expected_metre_numerator, denumerator = song.metre.split("/")
        expected_metre_numerator = int(expected_metre_numerator)
        denumerator = int(denumerator)

        check_metre_detection(
            metre_acc_data, song, result_metre, expected_metre_numerator, denumerator
        )

    summarize_tempo_detection(tempo_detector, tempo_acc_data, all_songs)
    summarize_metre_detection(metre_detector, metre_acc_data, all_songs)
    totalTime = time.time() - startTime
    logging.info(f"Total time: {totalTime}")


if __name__ == "__main__":
    # test_data_songs(CombFilterTempoDetector, SpectrogramMetreDetector)
    # test_data_songs_metre(SpectrogramMetreDetector)
    test_data_songs_tempo(CombFilterTempoDetector)
    write_settings()
