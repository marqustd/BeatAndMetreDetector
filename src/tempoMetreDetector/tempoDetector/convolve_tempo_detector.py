import logging
import numpy as np
from utilities import plots
import scipy.signal
from .base_tempo_detector import BaseTempoDetector
from .tempo_detector_data import TempoDetectorData


class ConvolveTempoDetector(BaseTempoDetector):
    def __str__(self):
        return "ConvolveTempoDetector"

    def detect_tempo(self, data: TempoDetectorData) -> int:
        n = len(data.filters_signals[0])
        nbands = len(data.bands_number)

        maxe = 0
        for bpm in range(data.min_bpm, data.max_bpm, data.accuracy):
            e = 0

            filterLength = 2
            nstep = np.floor(60 / bpm * data.sampling_frequency)
            percent_done = 100 * (bpm - data.min_bpm) / (data.max_bpm - data.min_bpm)
            fil = np.zeros(int(filterLength * nstep))

            logging.debug("%.2f" % percent_done, "%")

            for a in range(0, filterLength):
                fil[a * int(nstep)] = 1

            plots.draw_plot(fil, f"Timecomb bpm: {bpm}", "Sample/Time", "Amplitude")

            dftfil = np.fft.fft(fil)

            plots.drawCombFilterFftPlot(
                dftfil, f"Filter DFT {bpm}", data.sampling_frequency
            )
            for band in range(0, nbands - 1):
                filt = scipy.convolve(data.filters_signals[band], fil)
                f_filt = abs(np.fft.fft(filt))
                plots.draw_fft_plot(
                    f_filt, f"Convolve DFT {bpm}", data.sampling_frequency
                )

                x = abs(f_filt) ** 2
                e = e + sum(x)

            data.plot_dictionary[bpm] = e
            if e > maxe:
                sbpm = bpm
                maxe = e

        return sbpm
