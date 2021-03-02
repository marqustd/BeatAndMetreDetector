class BaseTempoDetector():
    def __str__(self):
        return "BaseTempoDetector"

    def detect_tempo(self, signal, accuracy: int, minBpm: int, maxBpm: int, bandsLimits, samplingFrequency, combFilterPulses, plotDictionary):
        return 0
