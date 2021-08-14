import numpy as np
import plots
import scipy.signal
from tempometredetector.metredetector.metre_enum import MetreEnum
from tempometredetector.metredetector.metre_detector_data import MetreDetectorData
from tempometredetector.metredetector.base_metre_detector import BaseMetreDetector


class ConvolveMetreDetector(BaseMetreDetector):
    __methods = []

    def __str__(self):
        return "ConvolveMetreDetector"

    def detect_metre(self, data: MetreDetectorData) -> MetreEnum:
        n = int(data.combFilterPulses * data.samplingFrequency * (60 / data.songTempo))
        nbands = len(data.bandLimits)

        self.__methods.append(self.__five_forth)
        self.__methods.append(self.__four_forth)
        self.__methods.append(self.__six_eigth)
        self.__methods.append(self.__three_forth)

        metres = {}
        for method in self.__methods:
            metre, metre_dft = method(
                data.songTempo, n, data.samplingFrequency, data.combFilterPulses
            )
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
                plots.draw_plot(f_filt, metrum, "Sample/Time", "Amplitude")
                x = abs(f_filt) ** 2
                e = e + sum(x)

            if e > maxe:
                song_metre = metrum
                maxe = e

        return song_metre

    def __four_forth(
        self, songTempo: int, n: int, samplingFrequency: int, combFilterPulses: int
    ):
        fil = np.zeros(int(4 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor(60 / songTempo * samplingFrequency)

        value = 1
        fil[int(1 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value

        plots.draw_plot(fil, "4\\4", "Sample/Time", "Amplitude")
        return "4\\4", fil

    def __three_forth(
        self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int
    ):
        fil = np.zeros(int(6 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor(60 / songTempo * samplingFrequency)

        value = 1
        fil[int(2 * nstep)] = 1 * value
        fil[int(5 * nstep)] = 1 * value

        plots.draw_plot(fil, "3\\4", "Sample/Time", "Amplitude")
        return "3\\4", fil

    def __five_forth(
        self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int
    ):
        fil = np.zeros(int(5 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor(60 / songTempo * samplingFrequency)

        value = 1
        fil[int(1 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value
        fil[int(4 * nstep)] = 1 * value

        plots.draw_plot(fil, "5\\4", "Sample/Time", "Amplitude")
        return "5\\4", fil

    def __six_eigth(
        self, songTempo: int, n: int, samplingFrequency: int, filter_pulses: int
    ):
        fil = np.zeros(int(3 * samplingFrequency * (60 / songTempo)))
        nstep = np.floor((60 / songTempo * samplingFrequency) / 2)

        value = 1
        fil[int(0 * nstep)] = 1 * value
        fil[int(3 * nstep)] = 1 * value

        plots.draw_plot(fil, "6\\8", "Sample/Time", "Amplitude")
        return "6\\8", fil