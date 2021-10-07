from tempometredetector.metredetector.metre_detector_data import MetreDetectorData
from .median_filter import *
from .bsm_calculator import *
import numpy as np
from scipy import signal
import settings


class SpectrogramTimeSignatureDetector:
    def detect_metre(self, data: MetreDetectorData):
        signal = data.signal
        sampling_frequency = data.sampling_frequency
        song_tempo = data.song_tempo
        beatDurationSample = self.__calculate_beat_duration(
            sampling_frequency, song_tempo
        )

        spectrogram, frequencies, times = self.__prepare_spectrogram(
            signal, sampling_frequency, beatDurationSample
        )
        spectrogram, frequencies = self.__down_sample_spectrogram(
            spectrogram, frequencies, settings.spectrogram_limit_frequency
        )

        spectrogram = self.__apply_median_filter(spectrogram)

        bsm = calculate_bsm(spectrogram, times, euclidian_distance)
        d = self.__calculate_diagonal_function(bsm)
        return self.__detect_metre(bsm, d)

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

    def __calculate_beat_duration(self, samplingFrequency, songTempo):
        beatDurationSec = 60 / songTempo
        beatDurationSample = int(beatDurationSec * samplingFrequency)
        return beatDurationSample

    def __prepare_spectrogram(self, sample, samplingFrequency, beatDurationSample):
        frequencies, times, spectrogram = signal.spectrogram(
            x=sample,
            fs=samplingFrequency,
            nperseg=int(beatDurationSample),
            noverlap=int(beatDurationSample / settings.noverlapRatio),
            mode="magnitude",
        )
        return spectrogram, frequencies, times

    def __down_sample_spectrogram(self, spectrogram, frequencies, limitFrequency):
        frequenciesLessThan = np.argwhere(frequencies < limitFrequency)
        lastIndex = frequenciesLessThan[-1, 0]
        frequencies = frequencies[0:lastIndex]
        spectrogram = spectrogram[0:lastIndex, :]
        return spectrogram, frequencies

    def __calculate_percusive_component(self, spectrogram, windowSize):
        percusive = median_filter(spectrogram, windowSize, 0)
        spectrogram = percusive
        return spectrogram

    def __calculate_harmonic_component(self, spectrogram, windowSize):
        harmonic = median_filter(spectrogram, 0, windowSize)
        spectrogram = harmonic
        return spectrogram

    def __calculate_diagonal_function(self, asm):
        diagonolasNumber = int(len(asm) / 2)
        diagonolasNumber = len(asm)
        d = np.zeros(diagonolasNumber)
        for i in range(diagonolasNumber):
            d[i] = np.average(np.diag(asm, i))

        for i in range(diagonolasNumber):
            d[i] = -d[i] + np.max(np.abs(d))
        return d

    def __detect_metre(self, asm, d):
        metreCandidates = 16
        lt = int(len(asm) / metreCandidates)
        t = np.zeros(metreCandidates)
        for c in range(2, metreCandidates, 1):
            for p in range(1, lt, 1):
                t[c] += (d[p * c]) / (1 - ((p - 1) / lt))

        t[0] = 0
        t[1] = 0

        metre = np.argmax(t)
        return metre


if __name__ == "__main__":
    detector = SpectrogramTimeSignatureDetector()
    detector.test_data_songs()
