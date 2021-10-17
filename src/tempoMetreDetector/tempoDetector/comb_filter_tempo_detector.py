import logging
import numpy as np
from utilities import plots
from .base_tempo_detector import BaseTempoDetector
from .tempo_detector_data import TempoDetectorData


class CombFilterTempoDetector(BaseTempoDetector):
    def __str__(self):
        return "CombFilterTempoDetector"

    def detect_tempo(self, detect_data: TempoDetectorData) -> int:
        sample_length = len(detect_data.filters_signals[0])
        bands_amount = len(detect_data.bands_number)
        comb_filter_ffts = self.__calculate_fft_of_filters(
            detect_data, sample_length, bands_amount
        )

        max_energy = 0
        for bpm in range(
            detect_data.min_bpm, detect_data.max_bpm, detect_data.accuracy
        ):
            this_bpm_energy = 0
            comb_filter_signal = np.zeros(sample_length)

            self.__prepare_comb_filter_signal(detect_data, bpm, comb_filter_signal)
            self.__write_progress(detect_data, bpm)

            this_bpm_energy = self.__calculate_this_bmp_energy(
                bands_amount,
                comb_filter_ffts,
                this_bpm_energy,
                comb_filter_signal,
                bpm,
                detect_data,
            )

            detect_data.plot_dictionary[bpm] = this_bpm_energy
            if this_bpm_energy > max_energy:
                song_bpm = bpm
                max_energy = this_bpm_energy

        return song_bpm

    def __calculate_this_bmp_energy(
        self,
        bands_amount,
        comb_filter_ffts,
        this_bpm_energy,
        comb_filter_signal,
        bpm,
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

    def __write_progress(self, detect_data: TempoDetectorData, bpm):
        percent_done = (
            100
            * (bpm - detect_data.min_bpm)
            / (detect_data.max_bpm - detect_data.min_bpm)
        )
        logging.debug("%.2f" % percent_done, "%")

    def __prepare_comb_filter_signal(
        self, detect_data: TempoDetectorData, bpm, filter_signal
    ):
        filter_step = np.floor(60 / bpm * detect_data.sampling_frequency)
        for a in range(0, detect_data.comb_filter_pulses):
            filter_signal[a * int(filter_step) + 1] = 1

    def __calculate_fft_of_filters(self, detect_data, sample_length, bands_amount):
        comb_filter_ffts = np.zeros([bands_amount, sample_length], dtype=complex)

        for band in range(0, bands_amount):
            comb_filter_ffts[band] = np.fft.fft(detect_data.filters_signals[band])
        return comb_filter_ffts
