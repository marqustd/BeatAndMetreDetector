from .median_filter import median_filter
import numpy as np


def separate_components(spectrogram, window_size: np.number):
    percussive_filter = median_filter(spectrogram, window_size, 0)
    harmonic_filter = median_filter(spectrogram, 0, window_size)

    harmonic = np.zeros(spectrogram.shape)
    percussive = np.zeros(spectrogram.shape)

    for x in range(len(spectrogram)):
        for y in range(len(spectrogram[0])):
            if harmonic_filter[x, y] > percussive_filter[x, y]:
                harmonic[x][y] = spectrogram[x, y]
            else:
                percussive[x][y] = spectrogram[x, y]

    return harmonic, percussive, harmonic_filter, percussive_filter
