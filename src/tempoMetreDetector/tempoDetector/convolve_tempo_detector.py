import logging
import numpy as np
from utilities import plots
import scipy.signal
from .base_tempo_detector import BaseTempoDetector
from .tempo_detector_data import TempoDetectorData
from tempometredetector.tempodetector import common


class ConvolveTempoDetector(BaseTempoDetector):
    def __str__(self):
        return "ConvolveTempoDetector"

    def detect_tempo(self, detect_data: TempoDetectorData):
        sample_length = len(detect_data.filters_signals[0])
        bands_amount = len(detect_data.bands_number)

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

            for band in range(0, bands_amount - 1):
                convoled = scipy.convolve(
                    detect_data.filters_signals[band], comb_filter_signal
                )
                convoled_fft = abs(np.fft.fft(convoled))
                plots.draw_fft_plot(
                    convoled_fft,
                    f"Convolve DFT {current_bpm}",
                    detect_data.sampling_frequency,
                )

                x = abs(convoled_fft) ** 2
                this_bpm_energy = this_bpm_energy + sum(x)

            detect_data.plot_dictionary[current_bpm] = this_bpm_energy
            if this_bpm_energy > max_energy:
                sbpm = current_bpm
                max_energy = this_bpm_energy

        return sbpm
