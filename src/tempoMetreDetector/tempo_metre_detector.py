import time

import numpy as np
import scipy.signal
import settings
from songreader import song_reader
from tempometredetector.metredetector.base_metre_detector import BaseMetreDetector
from tempometredetector.metredetector.metre_detector_data import MetreDetectorData
import logging
from utilities import plots

from tempometredetector.tempodetector import (
    BaseTempoDetector,
    TempoDetectorData,
)


class TempoMetreDetector:
    __tempo_detector: BaseTempoDetector
    __metre_detector = BaseMetreDetector

    def __init__(self, tempo_detector, metre_detector):
        self.__tempo_detector = tempo_detector
        self.__metre_detector = metre_detector

    def detect(self, tempo: int, metre: int, path: str):
        song_tempo = tempo
        song_metre = metre
        startTime = time.time()

        logging.debug(f"Detecting tempo and metre for song {path}...")

        signal, sampling_frequency = song_reader.read_song_fragment(
            path, settings.fragment_length
        )

        if self.__tempo_detector is not None:
            song_tempo = self.detect_tempo(sampling_frequency, signal)

        if self.__metre_detector is not None:
            song_metre = self.detect_metre(song_tempo, sampling_frequency, signal)

        totalTime = time.time() - startTime

        return song_tempo, song_metre, totalTime

    def detect_metre(self, song_tempo, samplingFrequency, signal):
        detector = self.__metre_detector()
        logging.debug(f"Detecting song's metre with method {detector}")

        metre_detector_data = MetreDetectorData(
            sampling_frequency=samplingFrequency,
            signal=signal,
            song_tempo=song_tempo,
        )

        metre = detector.detect_metre(metre_detector_data)
        return metre

    def detect_tempo(self, samplingFrequency, signal):
        detector = self.__tempo_detector()
        logging.info(f"Detecting song's tempo with method {detector}")
        resampled, samplingFrequency = self.__resample_signal(signal, samplingFrequency)

        filterBanks = self.__prepare_filterbanks(
            resampled, settings.band_limits, samplingFrequency
        )

        plots.draw_fft_plot(
            filterBanks[3], f"Sygnał z drugiego filtru piosenki", samplingFrequency
        )
        plots.draw_fft_plot(
            filterBanks[5], f"Sygnał z szóstego filtru piosenki", samplingFrequency
        )

        logging.debug(f"Hanning song...")
        hanningWindow = self.__hann(
            filterBanks, 0.2, settings.band_limits, samplingFrequency
        )
        plots.draw_plot(
            hanningWindow[1], f"Sygnał drugiego filtru piosenki po wygładzeniu"
        )

        logging.debug(f"Differentiating song...")
        diffrected = self.__diffrect(hanningWindow, len(settings.band_limits))
        plots.draw_plot(
            diffrected[1], "Pochodna wygładzonego sygnału z drugiego filtru piosenki"
        )

        logging.debug(f"First attempt...")
        plotDictionary = plots.prepare_plot_dictionary(
            settings.min_bpm, settings.max_bpm
        )

        firstAttemptTempoDetectorData = TempoDetectorData(
            diffrected,
            5,
            settings.min_bpm,
            settings.max_bpm,
            settings.band_limits,
            samplingFrequency,
            settings.comb_filter_pulses,
            plotDictionary,
        )

        songTempo = detector.detect_tempo(firstAttemptTempoDetectorData)

        logging.debug(f"Second attempt...")
        secondAttemptTempoDetectorData = TempoDetectorData(
            diffrected,
            1,
            songTempo - 5,
            songTempo + 5,
            settings.band_limits,
            samplingFrequency,
            settings.comb_filter_pulses,
            plotDictionary,
        )
        songTempo = detector.detect_tempo(secondAttemptTempoDetectorData)
        return songTempo

    def __resample_signal(self, signal, samplingFrequency):
        if settings.resample_signal:
            resampled = scipy.signal.resample(
                signal, int(len(signal) / settings.resample_ratio)
            )
            samplingFrequency /= settings.resample_ratio
        return resampled, samplingFrequency

    def __prepare_filterbanks(self, signal, bandlimits, samplingFrequency):
        dft = np.fft.fft(signal)
        n = len(dft)
        nbands = len(bandlimits)
        bl = np.zeros(nbands, int)
        br = np.zeros(nbands, int)

        for band in range(0, nbands - 1):
            bl[band] = np.floor(bandlimits[band] / samplingFrequency * n / 2) + 1
            br[band] = np.floor(bandlimits[band + 1] / samplingFrequency * n / 2)

        bl[0] = 0
        bl[nbands - 1] = (
            np.floor(bandlimits[nbands - 1] / samplingFrequency * n / 2) + 1
        )
        br[nbands - 1] = np.floor(n / 2)

        output = np.zeros([nbands, n], dtype=complex)

        for band in range(0, nbands):
            for hz in range(bl[band], br[band]):
                output[band, hz] = dft[hz]
            for hz in range(n - br[band], n - bl[band]):
                output[band, hz] = dft[hz]

        output[1, 1] = 0
        return output

    def __hann(self, signal, winLength, bandslimits, samplingFrequency):
        n = len(signal[0])
        nbands = len(bandslimits)
        hannlen = winLength * 2 * samplingFrequency
        hann = np.zeros(n)
        wave = np.zeros([nbands, n], dtype=complex)
        output = np.zeros([nbands, n], dtype=complex)
        freq = np.zeros([nbands, n], dtype=complex)
        filtered = np.zeros([nbands, n], dtype=complex)

        for a in range(1, int(hannlen)):
            hann[a] = (np.cos(a * np.pi / hannlen / 2)) ** 2

        for band in range(0, nbands):
            wave[band] = np.real(np.fft.ifft(signal[band]))

        for band in range(0, nbands):
            for j in range(0, n):
                if wave[band, j] < 0:
                    wave[band, j] = -wave[band, j]
            freq[band] = np.fft.fft(wave[band])

        for band in range(0, nbands):
            filtered[band] = freq[band] * np.fft.fft(hann)
            output[band] = np.real(np.fft.ifft(filtered[band]))

        return output

    def __diffrect(self, signal, nbands=6):
        n = len(signal[0])
        output = np.zeros([nbands, n], dtype=complex)

        for band in range(0, nbands):
            for j in range(5, n):
                d = signal[band, j] - signal[band, j - 1]
                if d > 0:
                    output[band, j] = d

        return output
