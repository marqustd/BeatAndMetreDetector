import numpy as np
import plots
import settings


class CombFilterNormalizedMetreDetector:
    __methods = []

    def __str__(self):
        return "CombFilterNormalizedMetreDetector"

    def detect_metre(self, signal, tempo: int, bandlimits, maxFreq, npulses):
        n = int(npulses * maxFreq * (60 / tempo))
        nbands = len(bandlimits)
        dft = np.zeros([nbands, n], dtype=complex)

        for band in range(0, nbands):
            dft[band] = np.fft.fft(signal[band, 0:n])
            plots.draw_plot(settings.drawPlots, signal[band], f"Signal[{band}]", "Sample/Time", "Amplitude")
            plots.draw_fft_plot(settings.drawFftPlots, dft[band], f"Signal[{band}] dft", maxFreq)
            plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft[band], f"Signal[{band}] dft", maxFreq)

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

    def __four_forth(self, tempo, n, sampling_frequency, filter_pulses):
        fil = np.zeros(n)
        nstep = np.floor(60 / tempo * sampling_frequency)
        index = 0
        bit = 0
        pulse = 1 / (np.floor(filter_pulses / 2))
        while index < n and bit < filter_pulses:
            value = pulse
            if bit % 2 == 0:
                value = 0

            fil[int(index)] = value
            index += nstep
            bit += 1

        filterSum = sum(abs(fil))
        print("Sum 4\\4 filter: ", filterSum)
        plots.draw_plot(settings.drawCombFilterPlots, fil, "4\\4 filter", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 4\\4 filter dft", sampling_frequency)
        energy = sum(abs(dft) ** 2)
        print("4\\4 filter energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("4\\4 filter energy normalized: ", energy)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 4\\4 filter normalized dft",
                                        sampling_frequency)
        return "4\\4", dft

    def __three_forth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(n)
        nstep = np.floor(60 / song_tempo * sampling_frequency)  # every third bit
        index = 0
        bit = 0

        pulse = 1 / (np.floor(filter_pulses / 3))

        while index < n and bit < filter_pulses:
            value = 0
            if bit % 3 == 2:
                value = pulse
            fil[int(index)] = value
            index += nstep
            bit += 1

        filterSum = sum(abs(fil))
        print("Sum 3\\4 filter: ", filterSum)
        plots.draw_plot(settings.drawCombFilterPlots, fil, "3\\4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 3\\4 filter dft", sampling_frequency)
        energy = sum(abs(dft) ** 2)
        print("3\\4 filter energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("3\\4 filter energy normalized: ", energy)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 3\\4 filter normalized dft",
                                        sampling_frequency)
        return "3\\4", dft

    def __five_forth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(n)
        nstep = np.floor(60 / song_tempo * sampling_frequency)  # every third bit
        index = 0
        bits = 0
        bit = 1

        pulse = 1 / (np.floor(filter_pulses / 5) * 3 + self.__rest_pulses(filter_pulses))

        while index < n and bits < filter_pulses:
            value = 0
            if bit == 2 or bit == 4 or bit == 5:
                value = pulse
            fil[int(index)] = value
            index += nstep
            bit += 1
            bits += 1
            if bit > 5:
                bit = 1

        filterSum = sum(abs(fil))
        print("Sum 5\\4 filter: ", filterSum)
        plots.draw_plot(settings.drawCombFilterPlots, fil, "5\\4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 5\\4 filter dft", sampling_frequency)
        energy = sum(abs(dft) ** 2)
        print("5\\4 filter energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("5\\4 filter energy normalized: ", energy)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 5\\4 filter normalized dft",
                                        sampling_frequency)
        return "5\\4", dft

    def __rest_pulses(self, filter_pulses):
        rest = filter_pulses % 5
        if rest == 0 or rest == 1:
            return 0
        elif rest == 2 or rest == 3:
            return 1
        return 2

    def __six_eigth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(n)
        pulses = (filter_pulses * 2 - 1) / 3
        nstep = np.floor((60 / song_tempo * sampling_frequency) / 2)
        pulse = 1 / pulses
        bit = 0
        index = 0

        while index < n and bit < (filter_pulses * 2)-1:
            value = pulse
            if bit % 3 > 0:
                value = 0
            fil[int(index)] = value
            index += nstep
            bit += 1

        filterSum = sum(abs(fil))
        print("Sum 6\\8 filter: ", filterSum)
        plots.draw_plot(settings.drawCombFilterPlots, fil, "6\\8", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 6\\8 filter dft", sampling_frequency)
        energy = sum(abs(dft) ** 2)
        print("6\\8 filter energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("6\\8 filter energy normalized: ", energy)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 6\\8 filter normalized dft",
                                        sampling_frequency)
        return "6\\8", dft
