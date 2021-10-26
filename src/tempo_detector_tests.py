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
import sys


def write_settings():
    for property, value in vars(settings).items():
        logging.info(f"{property} : {value}")


def test_data_songs_tempo(tempo_detector: BaseTempoDetector):
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


if __name__ == "__main__":
    args = sys.argv[1:]
    fragment_length = int(args[0])
    comb_filter_pulses = int(args[1])

    settings.comb_filter_pulses = comb_filter_pulses
    settings.fragment_length = fragment_length

    config_logger(
        f"results/tempo-comb-{settings.fragment_length}-{settings.comb_filter_pulses}.log"
    )

    test_data_songs_tempo(CombFilterTempoDetector)
