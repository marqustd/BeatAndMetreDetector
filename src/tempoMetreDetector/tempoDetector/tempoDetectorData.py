from typing import Dict
import numpy as np


class TempoDetectorData:
    signal: np.array
    accuracy: int
    minBpm: int
    maxBpm: int
    bandsLimits: int
    samplingFrequency: int
    combFilterPulses: int
    plotDictionary: Dict[int, int]

    def __init__(self, signal: np.array,
                 accuracy: int,
                 minBpm: int,
                 maxBpm: int,
                 bandsLimits: int,
                 samplingFrequency: int,
                 combFilterPulses: int,
                 plotDictionary: Dict[int, int]):
        self.signal = signal
        self.accuracy = accuracy
        self.minBpm = minBpm
        self.maxBpm = maxBpm
        self.bandsLimits = bandsLimits
        self.samplingFrequency = samplingFrequency
        self.combFilterPulses = combFilterPulses
        self.plotDictionary = plotDictionary
