import numpy as np
import plots
import scipy.signal
from .base_tempo_detector import BaseTempoDetector
from .tempo_detector_data import TempoDetectorData


class ConvolveTempoDetector(BaseTempoDetector):
    def __str__(self):
        return "ConvolveTempoDetector"

    def detect_tempo(self, data: TempoDetectorData) -> int:
        n = len(data.signal[0])
        nbands = len(data.bandsLimits)

        maxe = 0
        for bpm in range(data.minBpm, data.maxBpm, data.accuracy):
            e = 0

            filterLength = 2
            nstep = np.floor(60 / bpm * data.samplingFrequency)
            percent_done = 100 * (bpm - data.minBpm) / (data.maxBpm - data.minBpm)
            fil = np.zeros(int(filterLength * nstep))

            print("%.2f" % percent_done, "%")

            for a in range(0, filterLength):
                fil[a * int(nstep)] = 1

            plots.draw_plot(fil, f"Timecomb bpm: {bpm}", "Sample/Time", "Amplitude")

            dftfil = np.fft.fft(fil)

            plots.drawCombFilterFftPlot(
                dftfil, f"Filter DFT {bpm}", data.samplingFrequency
            )
            for band in range(0, nbands - 1):
                filt = scipy.convolve(data.signal[band], fil)
                f_filt = abs(np.fft.fft(filt))
                plots.draw_fft_plot(
                    f_filt, f"Convolve DFT {bpm}", data.samplingFrequency
                )

                x = abs(f_filt) ** 2
                e = e + sum(x)

            data.plotDictionary[bpm] = e
            if e > maxe:
                sbpm = bpm
                maxe = e

        return sbpm
