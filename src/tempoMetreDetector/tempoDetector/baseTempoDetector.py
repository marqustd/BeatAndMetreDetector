from  tempoMetreDetector.tempoDetector.tempoDetectorData import TempoDetectorData

class BaseTempoDetector():
    """Base class for detecting song's tempo.
    """
    def __str__(self):
        return "BaseTempoDetector"

    def detect_tempo(self, data: TempoDetectorData) -> int:
        return 0
