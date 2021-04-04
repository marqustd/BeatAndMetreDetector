from tempo.tempoDetectorData import TempoDetectorData
from metre import Metre

class BaseTempoDetector():
    """Base class for detecting song's tempo.
    """
    def __str__(self):
        return "BaseTempoDetector"

    def detect_tempo(self, data: TempoDetectorData) -> Metre.Metre:
        return Metre.Metre.METRE12
