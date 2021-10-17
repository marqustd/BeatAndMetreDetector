import logging
import numpy as np
from tempometredetector.tempodetector import common
from utilities import plots
from .base_tempo_detector import BaseTempoDetector
from .tempo_detector_data import TempoDetectorData


class CombFilterTempoDetector(BaseTempoDetector):
    def __str__(self):
        return "CombFilterTempoDetector"

    def detect_tempo(self, detect_data: TempoDetectorData):
        sample_length = len(detect_data.filters_signals[0])
        bands_amount = len(detect_data.bands_number)
        comb_filter_ffts = common.calculate_fft_of_filters(
            detect_data.filters_signals, sample_length, bands_amount
        )

        max_energy = 0
        for current_bpm in range(
            detect_data.min_bpm, detect_data.max_bpm, detect_data.accuracy
        ):
            this_bpm_energy = 0

            comb_filter_signal = common.prepare_comb_filter_signal(
                detect_data.sampling_frequency,
                detect_data.comb_filter_pulses,
                current_bpm,
                sample_length,
            )
            common.write_progress(detect_data.min_bpm, detect_data.max_bpm, current_bpm)

            this_bpm_energy = self.__calculate_this_bmp_energy(
                bands_amount,
                comb_filter_ffts,
                this_bpm_energy,
                comb_filter_signal,
                current_bpm,
                detect_data,
            )

            detect_data.plot_dictionary[current_bpm] = this_bpm_energy
            if this_bpm_energy > max_energy:
                song_bpm = current_bpm
                max_energy = this_bpm_energy

        return song_bpm

    def __calculate_this_bmp_energy(
        self,
        bands_amount: int,
        comb_filter_ffts,
        this_bpm_energy,
        comb_filter_signal,
        bpm: int,
        detect_data: TempoDetectorData,
    ):
        plots.draw_plot(
            comb_filter_signal,
            f"Sygnał filtru grzebieniowego  tempa {bpm}",
            "Próbki",
            "Amplituda",
        )
        filter_signal_fft = np.fft.fft(comb_filter_signal)
        plots.draw_comb_filter_fft_plot(
            filter_signal_fft,
            f"Widmo sygnału filtra tempa {bpm}",
            detect_data.sampling_frequency,
        )

        for band in range(0, bands_amount):
            x = (abs(filter_signal_fft * comb_filter_ffts[band])) ** 2
            this_bpm_energy = this_bpm_energy + sum(x)
        return this_bpm_energy
