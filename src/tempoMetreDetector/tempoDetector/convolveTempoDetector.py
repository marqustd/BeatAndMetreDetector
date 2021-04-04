from tempoMetreDetector.tempoDetector.tempoDetectorData import TempoDetectorData
from tempoMetreDetector.tempoDetector.baseTempoDetector import BaseTempoDetector
import numpy as np
import plots
import settings
import scipy.signal


class ConvolveTempoDetector(BaseTempoDetector):
    def __str__(self):
        return "ConvolveTempoDetector"

    def detect_tempo(self, data: TempoDetectorData) -> int:
        n = len(data.signal[0])
        nbands = len(data.bandsLimits)

        if data.minBpm < 60:
            minBpm = 60

        if data.maxBpm > 240:
            maxBpm = 240

        maxe = 0
        for bpm in range(minBpm, maxBpm, data.accuracy):
            e = 0

            filterLength = 2
            nstep = np.floor(60 / bpm * data.samplingFrequency)
            percent_done = 100 * (bpm - minBpm) / (maxBpm - minBpm)
            fil = np.zeros(int(filterLength * nstep))

            print("%.2f" % percent_done, "%")

            for a in range(0, filterLength):
                fil[a * int(nstep)] = 1

            plots.draw_plot(settings.drawMetreFilterPlots, fil,
                            f"Timecomb bpm: {bpm}", "Sample/Time", "Amplitude")

            dftfil = np.fft.fft(fil)

            plots.draw_comb_filter_fft_plot(settings.drawTempoFftPlots, dftfil, f"Filter DFT {bpm}",
                                            data.samplingFrequency)
            for band in range(0, nbands - 1):
                filt = scipy.convolve(data.signal[band], fil)
                f_filt = abs(np.fft.fft(filt))
                plots.draw_fft_plot(
                    settings.drawTempoFftPlots, f_filt, f"Convolve DFT {bpm}", data.samplingFrequency)

                x = abs(f_filt) ** 2
                e = e + sum(x)

            data.plotDictionary[bpm] = e
            if e > maxe:
                sbpm = bpm
                maxe = e

        return sbpm
