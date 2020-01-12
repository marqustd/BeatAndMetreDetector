from metre import combFilterMetreDetector
from tempo import combFilterTempoDetector


class TestCase:
    resampleSignal: bool
    resampleRatio: int
    combFilterPulses: int
    tempoDetector = combFilterTempoDetector.CombFilterTempoDetector()
    metreDetector = combFilterMetreDetector.CombFilterMetreDetector()

    def __init__(self, resample, resampleRatio, combFilterPulses, tempoDetector, metreDetector):
        self.resampleSignal = resample
        self.resampleRatio = resampleRatio
        self.combFilterPulses = combFilterPulses
        self.tempoDetector = tempoDetector
        self.metreDetector = metreDetector
