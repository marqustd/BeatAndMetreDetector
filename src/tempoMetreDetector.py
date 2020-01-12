import song
import settings
import time
from tempo import combFilterTempoDetector
from metre import convolveMetreDetector
import songReader
import scipy.signal
import plots
import numpy as np


class TempoMetreDetector:
    tempoDetector = combFilterTempoDetector.CombFilterTempoDetector()
    metreDetector = convolveMetreDetector.ConvolveMetreDetector()

    def __init__(self, tempoDetector, metreDetector):
        self.tempoDetector = tempoDetector
        self.metreDetector = metreDetector

    def detect_tempo_metre(self, song: song.Song):
        print(f'Detecting tempo and metre for song {song.name}...')
        startTime = time.time()
        signal, samplingFrequency = songReader.read_song(song.filepath)
        print(f'Signal read...')

        sample_length = settings.combFilterPulses * samplingFrequency
        seconds = sample_length * 4
        plots.draw_plot(settings.drawPlots, signal, f"Song: {song.name}", "Sample/Time", "Amplitude")
        song_length = signal.size

        start = int(np.floor(song_length / 2 - seconds / 2))
        stop = int(np.floor(song_length / 2 + seconds / 2))
        if start < 0:
            start = 0
        if stop > song_length:
            stop = song_length

        sample = signal[start:stop]
        plots.draw_plot(settings.drawPlots, sample, f"Sample of: {song.name}", "Sample/Time", "Amplitude")

        centred = self.__center_sample_to_beat(sample, sample_length)
        plots.draw_plot(settings.drawPlots, centred, f"Sample centred to beat: {song.name}", "Sample/Time", "Amplitude")

        if settings.resampleSignal:
            centred = scipy.signal.resample(centred, int(len(centred) / settings.resampleRatio))
            samplingFrequency /= settings.resampleRatio

        print(f'Preparing filterbank for song {song.name}...')
        filterBanks = self.__prepare_filterbanks(centred, settings.bandLimits, samplingFrequency)
        plots.draw_fft_plot(settings.drawPlots, filterBanks[1], f"Filterbank[{1}]{song.name}", samplingFrequency)

        print(f'Hanning song {song.name}...')
        hanningWindow = self.__hann(filterBanks, 0.2, settings.bandLimits, samplingFrequency)
        plots.draw_plot(settings.drawPlots, hanningWindow[1], f"Hanning Window: {song.name}", "Sample/Time",
                        "Amplitude")

        print(f'Differentiating song {song.name}...')
        diffrected = self.__diffrect(hanningWindow, len(settings.bandLimits))
        plots.draw_plot(settings.drawPlots, diffrected[1], f"Diffrected: {song.name}", "Sample/Time", "Amplitude")

        print(f"Detecting song's tempo {song.name} with method {self.tempoDetector}...")
        print(f'First attempt...')
        plotDictionary = plots.prepare_plot_dictionary(settings.minBpm, settings.maxBpm)

        first = self.tempoDetector.detect_tempo(diffrected,
                                                5,
                                                settings.minBpm,
                                                settings.maxBpm,
                                                settings.bandLimits,
                                                samplingFrequency,
                                                settings.combFilterPulses,
                                                plotDictionary)

        print(f'Second attempt...')
        songTempo = self.tempoDetector.detect_tempo(diffrected, 1, first - 5, first + 5, settings.bandLimits,
                                                    samplingFrequency, settings.combFilterPulses, plotDictionary)
        plots.draw_plot(settings.drawSongBpmEnergyPlot, list(plotDictionary.keys()), f"Tempo: {song.name}", "BPM",
                        "Energy", list(plotDictionary.values()))

        print(f"Detecting song's metre {song.name} with method {self.metreDetector}")
        metre = self.metreDetector.detect_metre(diffrected, songTempo, settings.bandLimits, samplingFrequency,
                                                settings.combFilterPulses)

        totalTime = time.time() - startTime

        return songTempo, metre, totalTime

    def __center_sample_to_beat(self, signal, required_length):
        n = len(signal)
        index = 0

        max = np.max(abs(signal))

        for i in range(0, n):
            if abs(signal[i]) > max * 0.9:
                index = i
                break

        lastindex = required_length
        lastindex += index
        if lastindex > n:
            lastindex = n
        if lastindex - index < required_length:
            index = index - (required_length - (lastindex - index))

        return signal[index:int(lastindex)]

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
        bl[nbands - 1] = np.floor(bandlimits[nbands - 1] / samplingFrequency * n / 2) + 1
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
