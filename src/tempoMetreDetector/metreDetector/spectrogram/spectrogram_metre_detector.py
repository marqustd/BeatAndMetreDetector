from tempometredetector.metredetector.base_metre_detector import BaseMetreDetector
from tempometredetector.metredetector.metre_detector_data import MetreDetectorData
from .median_filter import *
from .bsm_calculator import *
import numpy as np
from scipy import signal
import settings


class SpectrogramMetreDetector(BaseMetreDetector):
    def detect_metre(self, data: MetreDetectorData):
        signal = data.signal
        sampling_frequency = data.sampling_frequency
        song_tempo = data.song_tempo
        beat_duration_samples = self.__calculate_beat_duration(
            sampling_frequency, song_tempo
        )

        spectrogram, frequencies, times = self.__prepare_spectrogram(
            signal, sampling_frequency, beat_duration_samples
        )
        spectrogram, frequencies = self.__down_sample_spectrogram(
            spectrogram, frequencies, settings.spectrogram_limit_frequency
        )

        spectrogram = self.__apply_median_filter(spectrogram)

        bsm = calculate_bsm(spectrogram, times, settings.method)
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

    def __calculate_beat_duration(self, sampling_frequency, songTempo):
        seconds_in_minute = 60
        beat_duration_seconds = seconds_in_minute / songTempo
        beat_duration_samples = int(beat_duration_seconds * sampling_frequency)
        return beat_duration_samples

    def __prepare_spectrogram(self, sample, sampling_frequency, beat_duration_samples):
        frequencies, times, spectrogram = signal.spectrogram(
            x=sample,
            fs=sampling_frequency,
            nperseg=int(beat_duration_samples / settings.beat_split_ratio),
            noverlap=int(beat_duration_samples / settings.noverlap_ratio),
            mode="magnitude",
        )
        return spectrogram, frequencies, times

    def __down_sample_spectrogram(self, spectrogram, frequencies, limit_frequency):
        frequencies_less_than_limit = np.argwhere(frequencies < limit_frequency)
        last_index = frequencies_less_than_limit[-1, 0]
        frequencies = frequencies[0:last_index]
        spectrogram = spectrogram[0:last_index, :]
        return spectrogram, frequencies

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

        d = d[4:-4]

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
