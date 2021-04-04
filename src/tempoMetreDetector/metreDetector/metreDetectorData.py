import numpy as np


class MetreDetectorData:
    signal: np.array
    tempo: int
    bandlimits: int
    maxFreq: int
    npulses: int

    def __init__(self,
                 signal: np.array,
                 tempo: int,
                 bandlimits: int,
                 maxFreq: int,
                 npulses: int):
        self.signal = signal
        self.tempo = tempo
        self.bandlimits = bandlimits
        self.maxFreq = maxFreq
        self.npulses = npulses
