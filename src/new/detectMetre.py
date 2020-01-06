import scipy.signal
import numpy as np
import plots
import settings


class DetectMetre:
    def detectMetre(self, signal, tempo: int, bandlimits, maxFreq, npulses):
        length = len(signal[0])
        print(length)
        n = int(npulses * maxFreq * (60 / tempo))
        print(n)
        nbands = len(bandlimits)
        dft = np.zeros([nbands, n], dtype=complex)

        # Get signal in frequency domain
        for band in range(0, nbands):
            dft[band] = np.fft.fft(signal[band, 0:n])
            plots.draw_plot(settings.drawPlots, signal[band], f"Signal[{band}]", "Sample/Time", "Amplitude")
            plots.draw_fft_plot(settings.drawFftPlots, dft[band], f"Signal[{band}] dft", maxFreq)
            plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft[band], f"Signal[{band}] dft", maxFreq)

        metres = {}
        metre, metre_dft = self.__four_forth(tempo, n, maxFreq, npulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__three_forth(tempo, n, maxFreq, npulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__five_forth(tempo, n, maxFreq, npulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__six_eigth(tempo, n, maxFreq, npulses)
        metres[metre] = metre_dft
        # % Initialize max energy to zero
        maxe = 0
        for metrum in metres:
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
        energy = sum(abs(dft) ** 2)
        print("filter 4/4 energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("normalized filter 4/4 energy: ", energy)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 4/4 filter normalized dft", sampling_frequency)
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
        energy = sum(abs(dft) ** 2)
        print("filter 3/4 energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("normalized filter 3/4 energy: ", energy)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 3/4 filter normalized dft", sampling_frequency)
        return "3/4", dft

    def __five_forth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(n)
        nstep = np.floor(60 / song_tempo * sampling_frequency)  # every third bit
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
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 5/4 filter dft", sampling_frequency)
        energy = sum(abs(dft) ** 2)
        print("filter 5/4 energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("normalized filter 5/4 energy: ", energy)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 5/4 filter normalized dft", sampling_frequency)
        return "5/4", dft
    
    def __six_eigth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(n)
        nstep = np.floor((60 / song_tempo * sampling_frequency)/2)
        bit = 0
        index = 0
        while index < n and bit <= filter_pulses*2:
            value = 1
            if bit % 3 > 0:
                value = 0
            fil[int(index)] = value
            index += nstep
            bit += 1

        plots.draw_plot(settings.drawCombFilterPlots, fil, "6/8", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 6/8 filter dft", sampling_frequency)
        energy = sum(abs(dft) ** 2)
        print("filter 6/8 energy: ", energy)
        dft = dft / energy
        energy = sum(abs(dft) ** 2)
        print("normalized filter 6/8 energy: ", energy)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 6/8 filter normalized dft", sampling_frequency)
        return "6/8", dft