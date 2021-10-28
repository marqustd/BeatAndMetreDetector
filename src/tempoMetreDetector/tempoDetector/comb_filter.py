import logging
import numpy as np

import settings

comb_filter_signals = {}
comb_filter_ffts = {}


def reset_cache():
    comb_filter_signals.clear()
    comb_filter_ffts.clear()


def write_progress(min_bpm: int, max_bpm: int, current_bpm: int):
    percent_done = 100 * (current_bpm - min_bpm) / (max_bpm - min_bpm)
    logging.debug("%.2f" % percent_done, "%")


def get_comb_filter_signal(
    sample,
    sampling_frequency: int,
    bpm: int,
):
    comb_filter_signal = comb_filter_signals.get(bpm)
    if comb_filter_signal is None:
        comb_filter_signal = np.zeros(len(sample))
        filter_step = np.floor(60 / bpm * sampling_frequency)
        for a in range(0, settings.comb_filter_pulses):
            comb_filter_signal[a * int(filter_step) + 1] = 1
        comb_filter_signals[bpm] = comb_filter_signal

    return comb_filter_signal


def get_comb_filter_fft(sample, sampling_frequency: int, bpm: int):
    comb_filter_fft = comb_filter_ffts.get(bpm)
    if comb_filter_fft is None:
        comb_filter_signal = get_comb_filter_signal(sample, sampling_frequency, bpm)
        comb_filter_fft = np.fft.fft(comb_filter_signal)
        comb_filter_ffts[bpm] = comb_filter_fft

    return comb_filter_fft


def calculate_fft_of_filterbank(filterbank):
    comb_filter_ffts = np.zeros([len(filterbank), len(filterbank[0])], dtype=complex)

    for band in range(len(filterbank)):
        comb_filter_ffts[band] = np.fft.fft(filterbank[band])
    return comb_filter_ffts
