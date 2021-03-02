import metre
import tempo


class TestCase:
    resampleSignal: bool
    resampleRatio: int
    combFilterPulses: int
    tempoDetector: tempo.BaseTempoDetector.BaseTempoDetector
    metreDetector = metre.BaseMetreDetector.BaseMetreDetector

    def __init__(self, resample, resampleRatio, combFilterPulses, tempoDetector, metreDetector):
        self.resampleSignal = resample
        self.resampleRatio = resampleRatio
        self.combFilterPulses = combFilterPulses
        self.tempoDetector = tempoDetector
        self.metreDetector = metreDetector
