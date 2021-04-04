from typing import Dict
import numpy as np

class TempoDetectorData:
    signal : np.array
    accuracy: int 
    minBpm: int
    maxBpm: int
    bandsLimits: int
    samplingFrequency: int
    combFilterPulses: int
    plotDictionary: Dict[int, int]