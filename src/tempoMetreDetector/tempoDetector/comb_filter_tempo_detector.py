import numpy as np
import plots
from .base_tempo_detector import BaseTempoDetector
from .tempo_detector_data import TempoDetectorData


class CombFilterTempoDetector(BaseTempoDetector):
    def __str__(self):
        return "CombFilterTempoDetector"

    def detect_tempo(self, detect_data: TempoDetectorData) -> int:
        n = len(detect_data.signal[0])
        bands_amount = len(detect_data.bandsLimits)
        dft = self.__calculate_fft_of_filters(detect_data, n, bands_amount)

        maxEnergy = 0
        for bpm in range(detect_data.minBpm, detect_data.maxBpm, detect_data.accuracy):
            this_bpm_energy = 0
            comb_filter_signal = np.zeros(n)

            self.__prepare_comb_filter_signal(detect_data, bpm, comb_filter_signal)
            self.__write_progress(detect_data, bpm)

            this_bpm_energy = self.__calculate_this_bmp_energy(
                bands_amount, dft, this_bpm_energy, comb_filter_signal, bpm, detect_data
            )

            detect_data.plotDictionary[bpm] = this_bpm_energy
            if this_bpm_energy > maxEnergy:
                songBpm = bpm
                maxEnergy = this_bpm_energy

        return songBpm

    def __calculate_this_bmp_energy(
        self, bands_amount, dft, this_bpm_energy, comb_filter_signal, bpm, detect_data
    ):
        plots.drawPlot(
            comb_filter_signal,
            f"Sygnał filtru grzebieniowego  tempa {bpm}",
            "Próbki",
            "Amplituda",
        )
        dftfilter = np.fft.fft(comb_filter_signal)
        plots.drawCombFilterFftPlot(
            dftfilter,
            f"Widmo sygnału filtra tempa {bpm}",
            detect_data.samplingFrequency,
        )

        for band in range(0, bands_amount):
            x = (abs(dftfilter * dft[band])) ** 2
            this_bpm_energy = this_bpm_energy + sum(x)
        return this_bpm_energy

    def __write_progress(self, detect_data, bpm):
        percent_done = (
            100 * (bpm - detect_data.minBpm) / (detect_data.maxBpm - detect_data.minBpm)
        )
        print("%.2f" % percent_done, "%")

    def __prepare_comb_filter_signal(self, detect_data, bpm, fil):
        filter_step = np.floor(60 / bpm * detect_data.samplingFrequency)
        for a in range(0, detect_data.combFilterPulses):
            fil[a * int(filter_step) + 1] = 1

    def __calculate_fft_of_filters(self, detect_data, n, bands_amount):
        dft = np.zeros([bands_amount, n], dtype=complex)

        for band in range(0, bands_amount):
            dft[band] = np.fft.fft(detect_data.signal[band])
        return dft
