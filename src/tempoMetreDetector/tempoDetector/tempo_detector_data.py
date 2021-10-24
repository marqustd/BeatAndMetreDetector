from typing import Dict
import numpy as np
import settings


class TempoDetectorData:
    filterbank: np.array
    accuracy: int
    min_bpm: int
    max_bpm: int
    bands_number: int
    sampling_frequency: int
    comb_filter_pulses: int
    plot_dictionary: Dict[int, int]

    def __init__(
        self,
        signal: np.array,
        accuracy: int,
        minBpm: int,
        maxBpm: int,
        bandsLimits: int,
        samplingFrequency: int,
        combFilterPulses: int,
        plotDictionary: Dict[int, int],
    ):
        self.filterbank = signal
        self.accuracy = accuracy
        self.min_bpm = minBpm
        self.max_bpm = maxBpm
        self.bands_number = bandsLimits
        self.sampling_frequency = samplingFrequency
        self.comb_filter_pulses = combFilterPulses
        self.plot_dictionary = plotDictionary
        self.__checkTempoBandwidths()

    def __checkTempoBandwidths(self):
        if self.min_bpm < settings.min_bpm:
            self.min_bpm = settings.min_bpm

        if self.max_bpm > settings.max_bpm:
            self.max_bpm = settings.max_bpm
