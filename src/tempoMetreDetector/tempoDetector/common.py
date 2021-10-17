import logging
import numpy as np


def write_progress(min_bpm: int, max_bpm: int, current_bpm: int):
    percent_done = 100 * (current_bpm - min_bpm) / (max_bpm - min_bpm)
    logging.debug("%.2f" % percent_done, "%")


def prepare_comb_filter_signal(
    sampling_frequency, comb_filter_pulses, bpm: int, sample_length: int
):
    comb_filter_signal = np.zeros(sample_length)
    filter_step = np.floor(60 / bpm * sampling_frequency)
    for a in range(0, comb_filter_pulses):
        comb_filter_signal[a * int(filter_step) + 1] = 1

    return comb_filter_signal


def calculate_fft_of_filters(filters_signals, sample_length, bands_amount):
    comb_filter_ffts = np.zeros([bands_amount, sample_length], dtype=complex)

    for band in range(0, bands_amount):
        comb_filter_ffts[band] = np.fft.fft(filters_signals[band])
    return comb_filter_ffts
