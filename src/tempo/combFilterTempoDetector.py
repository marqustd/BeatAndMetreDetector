import numpy as np
import plots
import settings
from tempo import BaseTempoDetector

class CombFilterTempoDetector(BaseTempoDetector.BaseTempoDetector):
    def __str__(self):
        return "CombFilterTempoDetector"

    def detect_tempo(self, signal, accuracy: int, minBpm: int, maxBpm: int, bandsLimits, samplingFrequency,
                     combFilterPulses, plotDictionary):
        n = len(signal[0])
        bands_amount = len(bandsLimits)
        dft = np.zeros([bands_amount, n], dtype=complex)

        if minBpm < 60:
            minBpm = 60

        if maxBpm > 240:
            maxBpm = 240

        for band in range(0, bands_amount):
            dft[band] = np.fft.fft(signal[band])

        maxEnergy = 0
        for bpm in range(minBpm, maxBpm, accuracy):
            this_bpm_energy = 0
            fil = np.zeros(n)

            filter_step = np.floor(60 / bpm * samplingFrequency)
            percent_done = 100 * (bpm - minBpm) / (maxBpm - minBpm)
            print("%.2f" % percent_done, "%")

            for a in range(0, combFilterPulses):
                fil[a * int(filter_step) + 1] = 1

            plots.draw_plot(settings.drawTempoFilterPlots, fil, f"Sygnał filtru grzebieniowego  tempa {bpm}", "Próbki", "Amplituda")
            dftfil = np.fft.fft(fil)
            plots.draw_comb_filter_fft_plot(settings.drawTempoFftPlots, dftfil, f"Widmo sygnału filtra tempa {bpm}",
                                            samplingFrequency)

            for band in range(0, bands_amount):
                x = (abs(dftfil * dft[band])) ** 2
                this_bpm_energy = this_bpm_energy + sum(x)

            plotDictionary[bpm] = this_bpm_energy
            if this_bpm_energy > maxEnergy:
                songBpm = bpm
                maxEnergy = this_bpm_energy

        return songBpm
