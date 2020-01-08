import scipy.signal
import numpy as np
import plots
import settings


class DetectMetreConvolve:
    def detect_metre(self, signal, songTempo: int, bandLimits, samplingFrequency, combFilterPulses):
        length = len(signal[0])
        print(length)
        n = int(combFilterPulses * samplingFrequency * (60 / songTempo))
        print(n)
        nbands = len(bandLimits)

        for band in range(0, nbands):
            plots.draw_plot(settings.drawPlots, signal[band], f"band: {band}", "Sample/Time", "Amplitude")

        metres = {}
        metre, metre_dft = self.__four_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__three_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__five_forth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        metre, metre_dft = self.__six_eigth(songTempo, n, samplingFrequency, combFilterPulses)
        metres[metre] = metre_dft
        # % Initialize max energy to zero
        maxe = 0
        for metrum in metres:
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

    def __four_forth(self, songTempo: int, n: int, samplingFrequency: int, combFilterPulses: int):
        fil = np.zeros(int(4 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor(60 / songTempo * samplingFrequency)

        value = 1
        fil[int(1 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value

        plots.draw_plot(settings.drawCombFilterPlots, fil, "4/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 4/4 filter dft", samplingFrequency)
        return "4/4", fil

    def __three_forth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(int(3 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor(60 / songTempo * samplingFrequency)

        value = 1
        fil[int(2 * nstep)] = 1 * value

        plots.draw_plot(settings.drawCombFilterPlots, fil, "3/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 3/4 filter dft", samplingFrequency)
        return "3/4", fil

    def __five_forth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(int(5 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor(60 / songTempo * samplingFrequency)

        value = 1
        fil[int(1 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value
        fil[int(4 * nstep)] = 1 * value

        plots.draw_plot(settings.drawCombFilterPlots, fil, "5/4", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 5/4 filter dft", samplingFrequency)
        return "5/4", fil

    def __six_eigth(self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int):
        fil = np.zeros(int(3 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor((60 / songTempo * samplingFrequency) / 2)

        value = 1
        fil[int(0 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value

        plots.draw_plot(settings.drawCombFilterPlots, fil, "6/8", "Sample/Time", "Amplitude")
        dft = np.fft.fft(fil)
        plots.draw_comb_filter_fft_plot(settings.drawFftPlots, dft, f"Metre 6/8 filter dft", samplingFrequency)
        return "6/8", fil
