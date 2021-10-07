from tempometredetector.metredetector import base_metre_detector, metre_enum
import time
from typing import Tuple

import numpy as np
import plots
import scipy.signal
import settings
from songreader import song_reader, Song
from tempometredetector.metredetector.metre_detector_data import MetreDetectorData

from tempometredetector.tempodetector import (
    BaseTempoDetector,
    TempoDetectorData,
)


class TempoMetreDetector:
    tempoDetector: BaseTempoDetector
    metreDetector: base_metre_detector

    def __init__(self, tempoDetector, metreDetector):
        self.tempoDetector = tempoDetector
        self.metreDetector = metreDetector

    def detect_tempo_metre(self, song: Song):
        print(f"Detecting tempo and metre for song {song.name}...")
        startTime = time.time()
        signal, samplingFrequency = song_reader.read_song_fragment(song.filepath)

        resampled, samplingFrequency = self.__resample_signal(signal, samplingFrequency)

        songTempo = self.detect_tempo(song, samplingFrequency, resampled)

        print(f"Detecting song's metre {song.name} with method {self.metreDetector}")
        metreDeteCtorData = MetreDetectorData(
            diffrected,
            songTempo,
            settings.band_limits,
            samplingFrequency,
            settings.comb_filter_pulses,
        )

        metre = self.metreDetector.detect_metre(metreDeteCtorData)

        totalTime = time.time() - startTime

        plots.drawPlot(
            list(plotDictionary.keys()),
            f"Rozkład energii iloczynu widma sygnału z filtrem\n o określonej częstotliwości impulsów w piosence",
            "BPM",
            "Energy",
            list(plotDictionary.values()),
        )
        return songTempo, metre, totalTime

    def detect_tempo(self, song, samplingFrequency, resampled):
        filterBanks = self.__prepare_filterbanks(
            resampled, settings.band_limits, samplingFrequency
        )
        plots.drawFftPlot(
            filterBanks[3], f"Sygnał z drugiego filtru piosenki", samplingFrequency
        )
        plots.drawFftPlot(
            filterBanks[5], f"Sygnał z szóstego filtru piosenki", samplingFrequency
        )

        print(f"Hanning song {song.name}...")
        hanningWindow = self.__hann(
            filterBanks, 0.2, settings.band_limits, samplingFrequency
        )
        plots.drawPlot(
            hanningWindow[1], f"Sygnał drugiego filtru piosenki po wygładzeniu"
        )

        print(f"Differentiating song {song.name}...")
        diffrected = self.__diffrect(hanningWindow, len(settings.band_limits))
        plots.drawPlot(
            diffrected[1], "Pochodna wygładzonego sygnału z drugiego filtru piosenki"
        )

        print(f"Detecting song's tempo {song.name} with method {self.tempoDetector}...")
        print(f"First attempt...")
        plotDictionary = plots.preparePlotDictionary(settings.min_bpm, settings.max_bpm)

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

        songTempo = self.tempoDetector.detect_tempo(firstAttemptTempoDetectorData)

        print(f"Second attempt...")
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
        songTempo = self.tempoDetector.detect_tempo(secondAttemptTempoDetectorData)
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
