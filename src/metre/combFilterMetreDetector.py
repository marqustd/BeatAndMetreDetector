import numpy as np
import plots
import settings


class CombFilterMetreDetector:
    __methods = []

    def __str__(self):
        return "CombFilterMetreDetector"

    def detect_metre(self, signal, tempo: int, bandlimits, maxFreq, npulses):
        n = int(npulses * maxFreq * (60 / tempo))
        nbands = len(bandlimits)
        dft = np.zeros([nbands, n], dtype=complex)

        # Get signal in frequency domain
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

        # % Initialize max energy to zero
        maxe = 0
        done = 0
        todo = len(metres.keys())
        for metrum in metres:
            done += 1
            percent_done = 100 * done / todo
            print("%.2f" % percent_done, "%")

            # % Initialize energy and filter to zero(s)
            e = 0

            for band in range(0, nbands):
                x = (abs(metres[metrum] * dft[band])) ** 2
                e = e + sum(x)

            # If greater than all previous energies, set current bpm to the bpm of the signal
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

        plots.draw_plot(settings.drawCombFilterPlots, fil, "4/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 4/4 filter dft", sampling_frequency)
        return "4/4", dft

    def __three_forth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(n)
        nstep = np.floor(60 / song_tempo * sampling_frequency)  # every third bit
        index = 0
        bit = 0
        while index < n and bit <= filter_pulses:
            value = 1
            if bit % 3 > 0:
                value = 0
            fil[int(index)] = value
            index += nstep
            bit += 1

        plots.draw_plot(settings.drawCombFilterPlots, fil, "3/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 3/4 filter dft", sampling_frequency)
        return "3/4", dft

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

        plots.draw_plot(settings.drawCombFilterPlots, fil, "5/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        return "5/4", dft

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

        plots.draw_plot(settings.drawCombFilterPlots, fil, "6/8", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 6/8 filter dft", sampling_frequency)
        return "6/8", dft
