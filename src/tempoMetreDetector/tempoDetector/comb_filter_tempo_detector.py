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
        filterbank_ffts = common.calculate_fft_of_filterbank(detect_data.filterbank)

        max_energy = 0
        for current_bpm in range(
            detect_data.min_bpm, detect_data.max_bpm, detect_data.accuracy
        ):
            this_bpm_energy = 0

            common.write_progress(detect_data.min_bpm, detect_data.max_bpm, current_bpm)

            this_bpm_energy = self.__calculate_this_bmp_energy(
                filterbank_ffts,
                this_bpm_energy,
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
        comb_filter_ffts,
        this_bpm_energy,
        bpm: int,
        detect_data: TempoDetectorData,
    ):
        filter_signal_fft = common.get_comb_filter_fft(
            detect_data.sampling_frequency, bpm
        )
        plots.draw_comb_filter_fft_plot(
            filter_signal_fft,
            f"Widmo sygnału filtra tempa {bpm}",
            detect_data.sampling_frequency,
        )

        for band in range(0, len(comb_filter_ffts)):
            x = (abs(filter_signal_fft * comb_filter_ffts[band])) ** 2
            this_bpm_energy = this_bpm_energy + sum(x)
        return this_bpm_energy
