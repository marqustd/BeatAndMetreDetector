import scipy.signal
import numpy as np
import plots
import settings


class ConvolveNormalizedMetreDetector:
    def __str__(self):
        return "ConvolveNormalizedMetreDetector"

    def detect_metre(self, signal, tempo: int, bandlimits, maxFreq, npulses):
        length = len(signal[0])
        n = int(npulses * maxFreq * (60 / tempo))
        nbands = len(bandlimits)

        for band in range(0, nbands):
            plots.draw_plot(settings.drawPlots, signal[band], f"Band: {band}", "Sample/Time", "Amplitude")

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
        done = 0
        todo = len(metres.keys())
        for metrum in metres:
            done += 1
            percent_done = 100 * done / todo
            print("%.2f" % percent_done, "%")

            # % Initialize energy and filter to zero(s)
            e = 0

            for band in range(0, nbands):
                filt = scipy.convolve(signal[band], metres[metrum])
                f_filt = abs(np.fft.fft(filt))
                plots.draw_plot(settings.drawPlots, f_filt, metrum, "Sample/Time", "Amplitude")
                x = abs(f_filt) ** 2
                e = e + sum(x)

            # If greater than all previous energies, set current bpm to the bpm of the signal
            if e > maxe:
                song_metre = metrum
                maxe = e

        return song_metre

    def __four_forth(self, song_tempo: int, n: int, sampling_frequency: int, npulses: int):
        fil = np.zeros(int(4 * sampling_frequency * (60 / song_tempo)))
        nstep = np.floor(60 / song_tempo * sampling_frequency)

        value = 1 / 2
        fil[int(1 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value

        plots.draw_plot(settings.drawCombFilterPlots, fil, "4/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 4/4 filter dft", sampling_frequency)
        return "4/4", fil

    def __three_forth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(int(3 * sampling_frequency * (60 / song_tempo)))
        nstep = np.floor(60 / song_tempo * sampling_frequency)

        value = 1 / 1
        fil[int(2 * nstep)] = 1 * value

        plots.draw_plot(settings.drawCombFilterPlots, fil, "3/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 3/4 filter dft", sampling_frequency)
        return "3/4", fil

    def __five_forth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(int(5 * sampling_frequency * (60 / song_tempo)))
        nstep = np.floor(60 / song_tempo * sampling_frequency)

        value = 1 / 3
        fil[int(1 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value
        fil[int(4 * nstep)] = 1 * value

        plots.draw_plot(settings.drawCombFilterPlots, fil, "5/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 5/4 filter dft", sampling_frequency)
        return "5/4", fil

    def __six_eigth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(int(3 * sampling_frequency * (60 / song_tempo)))
        nstep = np.floor((60 / song_tempo * sampling_frequency) / 2)

        value = 1 / 2
        fil[int(0 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value

        plots.draw_plot(settings.drawCombFilterPlots, fil, "6/8", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 6/8 filter dft", sampling_frequency)
        return "6/8", fil
