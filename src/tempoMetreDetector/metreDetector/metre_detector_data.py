import numpy as np


class MetreDetectorData:
    signal: np.array
    sampling_frequency: int
    song_tempo: int

    def __init__(self, signal: np.array, song_tempo: int, sampling_frequency: int):
        self.signal = signal
        self.song_tempo = song_tempo
        self.sampling_frequency = sampling_frequency
