from tempometredetector.metredetector.base_metre_detector import BaseMetreDetector
from tempometredetector.metredetector.metre_detector_data import MetreDetectorData
from .median_filter import *
from .bsm_calculator import *
import numpy as np
from scipy import signal
import settings


class SpectrogramMetreDetector(BaseMetreDetector):
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "SpectrogramMetreDetector"

    def detect_metre(self, data: MetreDetectorData):
        signal = data.signal
        sampling_frequency = data.sampling_frequency
        song_tempo = data.song_tempo

        spectrogram = settings.spectrogram_function(data)

        spectrogram = self.__apply_median_filter(spectrogram)

        bsm = calculate_bsm(spectrogram, settings.method)
        d = self.__calculate_diagonal_function(bsm)
        return self.__detect_metre(d)

    def __apply_median_filter(self, spectrogram):
        if settings.median_filter == settings.MedianFilterEnum.PERCUSIVE:
            spectrogram = self.__calculate_percusive_component(
                spectrogram, settings.median_filter_window_size
            )

        elif settings.median_filter == settings.MedianFilterEnum.HARMONIC:
            spectrogram = self.__calculate_harmonic_component(
                spectrogram, settings.median_filter_window_size
            )

        return spectrogram

    def __calculate_percusive_component(self, spectrogram, window_size):
        percusive = median_filter(spectrogram, window_size, 0)
        spectrogram = percusive
        return spectrogram

    def __calculate_harmonic_component(self, spectrogram, window_size):
        harmonic = median_filter(spectrogram, 0, window_size)
        spectrogram = harmonic
        return spectrogram

    def __calculate_diagonal_function(self, asm):
        diagonals_number = len(asm)
        d = np.zeros(diagonals_number)
        for i in range(diagonals_number):
            d[i] = np.average(np.diag(asm, i))

        # d = d[4:-4]

        for i in range(len(d)):
            d[i] = -d[i] + np.max(np.abs(d))
        return d

    def __detect_metre(self, d):
        metre_candidates = settings.metre_candidates
        lt = int(len(d) / metre_candidates)
        t = np.zeros(metre_candidates)
        for c in range(2, metre_candidates, 1):
            for p in range(1, lt, 1):
                t[c] += (d[p * c]) / (1 - ((p - 1) / lt))

        t[0] = 0
        t[1] = 0

        metre = np.argmax(t)
        return metre


if __name__ == "__main__":
    detector = SpectrogramMetreDetector()
    detector.test_data_songs()
