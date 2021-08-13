import numpy as np


class MetreDetectorData:
    signal: np.array
    tempo: int
    bandlimits: int
    maxFreq: int
    npulses: int

    def __init__(
        self,
        signal: np.array,
        tempo: int,
        band_limits: int,
        max_freq: int,
        npulses: int,
    ):
        self.signal = signal
        self.tempo = tempo
        self.bandlimits = band_limits
        self.maxFreq = max_freq
        self.npulses = npulses
