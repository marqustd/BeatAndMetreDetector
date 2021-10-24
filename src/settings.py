from enum import Enum, auto

from tempometredetector.metredetector.spectrogram.bsm_calculator import (
    euclidian_distance,
    cosine_distance,
    kullback_leibler,
)
from tempometredetector.metredetector.spectrogram.spectrogram_provider import (
    get_mffc,
    get_standard_spectrogram,
)


class MedianFilterEnum(Enum):
    NONE = auto()
    PERCUSIVE = auto()
    HARMONIC = auto()


# fragment
beat_treshold = 0.9
fragment_length = 25

# comb filters
band_limits = [0, 200, 400, 800, 1600, 3200, 4000]
comb_filter_pulses = 8
min_bpm = 60
max_bpm = 240

# resampling
resample_signal = True
resample_ratio = 4

# plots
draw_plots = False
draw_tempo_fft_plots = True
draw_metre_fft_plots = True
draw_tempo_filter_plots = True
draw_metre_filter_plots = True
draw_song_bpm_energy_plots = True

# metre
spectrogram_limit_frequency = band_limits[-1]
median_filter_window_size = 701
noverlap_ratio = 64
median_filter = MedianFilterEnum.NONE
method = euclidian_distance
metre_candidates = 12
beat_split_ratio = 1
spectrogram_function = get_mffc
