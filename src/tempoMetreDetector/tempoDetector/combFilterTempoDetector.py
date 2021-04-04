import numpy as np
import plots
from tempoMetreDetector.tempoDetector.baseTempoDetector import \
    BaseTempoDetector
from tempoMetreDetector.tempoDetector.tempoDetectorData import \
    TempoDetectorData


class CombFilterTempoDetector(BaseTempoDetector):
    def __str__(self):
        return "CombFilterTempoDetector"

    def detectTempo(self, data: TempoDetectorData) -> int:
        n = len(data.signal[0])
        bands_amount = len(data.bandsLimits)
        dft = np.zeros([bands_amount, n], dtype=complex)

        for band in range(0, bands_amount):
            dft[band] = np.fft.fft(data.signal[band])

        maxEnergy = 0
        for bpm in range(data.minBpm, data.maxBpm, data.accuracy):
            this_bpm_energy = 0
            fil = np.zeros(n)

            filter_step = np.floor(60 / bpm * data.samplingFrequency)
            percent_done = 100 * (bpm - data.minBpm) / (data.maxBpm - data.minBpm)
            print("%.2f" % percent_done, "%")

            for a in range(0, data.combFilterPulses):
                fil[a * int(filter_step) + 1] = 1

            plots.drawPlot(fil,
                            f"Sygnał filtru grzebieniowego  tempa {bpm}", "Próbki", "Amplituda")
            dftfil = np.fft.fft(fil)
            plots.drawCombFilterFftPlot(dftfil, f"Widmo sygnału filtra tempa {bpm}",
                                            data.samplingFrequency)

            for band in range(0, bands_amount):
                x = (abs(dftfil * dft[band])) ** 2
                this_bpm_energy = this_bpm_energy + sum(x)

            data.plotDictionary[bpm] = this_bpm_energy
            if this_bpm_energy > maxEnergy:
                songBpm = bpm
                maxEnergy = this_bpm_energy

        return songBpm
