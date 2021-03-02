import numpy as np
import plots
import settings
from metre import BaseMetreDetector, Metre

class CombFilterMetreDetector(BaseMetreDetector.BaseMetreDetector):
    __methods = []

    def __str__(self):
        return "CombFilterMetreDetector"

    def detect_metre(self, signal, tempo: int, bandlimits, maxFreq, npulses) -> Metre.Metre:
        n = int(npulses * maxFreq * (60 / tempo))
        nbands = len(bandlimits)
        dft = np.zeros([nbands, n], dtype=complex)

        for band in range(0, nbands):
            dft[band] = np.fft.fft(signal[band, 0:n])

        self.__methods.append(self.__five_forth)
        self.__methods.append(self.__four_forth)
        self.__methods.append(self.__six_eigth)
        self.__methods.append(self.__three_forth)

        metres = {}
        for method in self.__methods:
            metre, metre_dft = method(tempo, n, maxFreq, npulses)
            metres[metre] = metre_dft

        maxe = 0
        done = 0
        todo = len(metres.keys())
        for metrum in metres:
            done += 1
            percent_done = 100 * done / todo
            print("%.2f" % percent_done, "%")

            e = 0

            for band in range(0, nbands):
                x = (abs(metres[metrum] * dft[band])) ** 2
                e = e + sum(x)

            if e > maxe:
                song_metre = metrum
                maxe = e

        return song_metre

    def __four_forth(self, tempo, n, sampling_frequency, npulses):
        fil = np.zeros(n)
        nstep = np.floor(60 / tempo * sampling_frequency)
        index = 0
        bit = 0
        while index < n and bit <= npulses:
            value = 1
            if bit % 2 > 0:
                value = 0

            fil[int(index)] = value
            index += nstep
            bit += 1

        plots.draw_plot(settings.drawMetreFilterPlots,
                        fil, "Sygnał filtra metrum 4\\4")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(
            settings.drawMetreFftPlots, dft, f"Metre 4\\4 filter dft", sampling_frequency)
        return "4\\4", dft

    def __three_forth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(n)
        # every third bit
        nstep = np.floor(60 / song_tempo * sampling_frequency)
        index = 0
        bit = 0
        while index < n and bit <= filter_pulses:
            value = 1
            if bit % 3 > 0:
                value = 0
            fil[int(index)] = value
            index += nstep
            bit += 1

        plots.draw_plot(settings.drawMetreFilterPlots,
                        fil, "Sygnał filtra metrum  3\\4")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(
            settings.drawMetreFftPlots, dft, f"Filtr metrum 3\\4", sampling_frequency)
        return "3\\4", dft

    def __five_forth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(n)
        nstep = np.floor(60 / song_tempo * sampling_frequency)
        index = 0
        bits = 0
        bit = 1
        while index < n and bits <= filter_pulses:
            value = 0
            if bit == 2 or bit == 4 or bit == 5:
                value = 1
            fil[int(index)] = value
            index += nstep
            bit += 1
            bits += 1
            if bit > 5:
                bit = 1

        plots.draw_plot(settings.drawMetreFilterPlots,
                        fil, "Sygnał filtra metrum 5\\4")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(
            settings.drawMetreFftPlots, dft, f"Metre 5\\4 filter dft", sampling_frequency)
        return "5\\4", dft

    def __six_eigth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(n)
        nstep = np.floor((60 / song_tempo * sampling_frequency) / 2)
        bit = 0
        index = 0
        while index < n and bit <= filter_pulses * 2:
            value = 1
            if bit % 3 > 0:
                value = 0
            fil[int(index)] = value
            index += nstep
            bit += 1

        plots.draw_plot(settings.drawMetreFilterPlots,
                        fil, "Sygnał filtra metrum  6\\8")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(
            settings.drawMetreFftPlots, dft, f"Metre 6\\8 filter dft", sampling_frequency)
        return "6\\8", dft
