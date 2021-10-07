from enum import Enum, auto


class MedianFilterEnum(Enum):
    NONE = auto()
    PERCUSIVE = auto()
    HARMONIC = auto()


# comb filters
band_limits = [0, 200, 400, 800, 1600, 3200, 6400]
comb_filter_pulses = 8
min_bpm = 60
max_bpm = 240
fragment_length = 30

# resampling
resample_signal = True
resample_ratio = 4

# plots
draw_plots = True
draw_tempo_fft_plots = True
draw_metre_fft_plots = True
draw_tempo_filter_plots = True
draw_metre_filter_plots = True
draw_song_bpm_energy_plots = True

# metre
spectrogram_limit_frequency = band_limits[-1]
median_filter_window_size = 201
noverlapRatio = 32
median_filter = MedianFilterEnum.NONE
