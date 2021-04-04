import scipy.signal
import numpy as np
import plots
import settings
from tempoMetreDetector.metreDetector.metreEnum import MetreEnum
from tempoMetreDetector.metreDetector.baseMetreDetector import BaseMetreDetector
from tempoMetreDetector.metreDetector.metreDetectorData import MetreDetectorData


class ConvolveNormalizedMetreDetector(BaseMetreDetector.BaseMetreDetector):
    __methods = []

    def __str__(self):
        return "ConvolveNormalizedMetreDetector"

    def detect_metre(self, data: MetreDetectorData) -> MetreEnum:
        n = int(data.npulses * data.maxFreq * (60 / data.tempo))
        nbands = len(data.bandlimits)

        self.__methods.append(self.__five_forth)
        self.__methods.append(self.__four_forth)
        self.__methods.append(self.__six_eigth)
        self.__methods.append(self.__three_forth)

        metres = {}
        for method in self.__methods:
            metre, metre_dft = method(
                data.tempo, n, data.maxFreq, data.npulses)
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
                filt = scipy.convolve(data.signal[band], metres[metrum])
                f_filt = abs(np.fft.fft(filt))
                plots.draw_plot(settings.drawMetreFftPlots,
                                f_filt, metrum, "Sample/Time", "Amplitude")
                x = abs(f_filt) ** 2
                e = e + sum(x)

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

        plots.draw_plot(settings.drawMetreFilterPlots, fil,
                        "4\\4", "Sample/Time", "Amplitude")
        return "4\\4", fil

    def __three_forth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(int(6 * sampling_frequency * (60 / song_tempo)))
        nstep = np.floor(60 / song_tempo * sampling_frequency)

        value = 1 / 2
        fil[int(2 * nstep)] = 1 * value
        fil[int(5 * nstep)] = 1 * value

        plots.draw_plot(settings.drawMetreFilterPlots, fil,
                        "3\\4", "Sample/Time", "Amplitude")
        return "3\\4", fil

    def __five_forth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(int(5 * sampling_frequency * (60 / song_tempo)))
        nstep = np.floor(60 / song_tempo * sampling_frequency)

        value = 1 / 3
        fil[int(1 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value
        fil[int(4 * nstep)] = 1 * value

        plots.draw_plot(settings.drawMetreFilterPlots, fil,
                        "5\\4", "Sample/Time", "Amplitude")
        return "5\\4", fil

    def __six_eigth(self, song_tempo: int, n: int, sampling_frequency: int, filter_pulses: int):
        fil = np.zeros(int(3 * sampling_frequency * (60 / song_tempo)))
        nstep = np.floor((60 / song_tempo * sampling_frequency) / 2)

        value = 1 / 2
        fil[int(0 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value

        plots.draw_plot(settings.drawMetreFilterPlots, fil,
                        "6\\8", "Sample/Time", "Amplitude")
        return "6\\8", fil
