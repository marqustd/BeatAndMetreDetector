from tempoMetreDetector.tempoDetector.tempoDetectorData import TempoDetectorData
from tempoMetreDetector.tempoDetector.baseTempoDetector import BaseTempoDetector
import numpy as np
import plots
import settings


class CombFilterTempoDetector(BaseTempoDetector):
    def __str__(self):
        return "CombFilterTempoDetector"

    def detect_tempo(self, data: TempoDetectorData) -> int:
        n = len(data.signal[0])
        bands_amount = len(data.bandsLimits)
        dft = np.zeros([bands_amount, n], dtype=complex)

        if data.minBpm < 60:
            minBpm = 60

        if data.maxBpm > 240:
            maxBpm = 240

        for band in range(0, bands_amount):
            dft[band] = np.fft.fft(data.signal[band])

        maxEnergy = 0
        for bpm in range(minBpm, maxBpm, data.accuracy):
            this_bpm_energy = 0
            fil = np.zeros(n)

            filter_step = np.floor(60 / bpm * data.samplingFrequency)
            percent_done = 100 * (bpm - minBpm) / (maxBpm - minBpm)
            print("%.2f" % percent_done, "%")

            for a in range(0, data.combFilterPulses):
                fil[a * int(filter_step) + 1] = 1

            plots.draw_plot(settings.drawTempoFilterPlots, fil,
                            f"Sygnał filtru grzebieniowego  tempa {bpm}", "Próbki", "Amplituda")
            dftfil = np.fft.fft(fil)
            plots.draw_comb_filter_fft_plot(settings.drawTempoFftPlots, dftfil, f"Widmo sygnału filtra tempa {bpm}",
                                            data.samplingFrequency)

            for band in range(0, bands_amount):
                x = (abs(dftfil * dft[band])) ** 2
                this_bpm_energy = this_bpm_energy + sum(x)

            data.plotDictionary[bpm] = this_bpm_energy
            if this_bpm_energy > maxEnergy:
                songBpm = bpm
                maxEnergy = this_bpm_energy

        return songBpm
