from tempoMetreDetector.tempoDetector.tempoDetectorData import TempoDetectorData
import settings


class BaseTempoDetector():
    """Base class for detecting song's tempo.
    """

    def __str__(self):
        return "BaseTempoDetector"

    def detectTempo(self, data: TempoDetectorData) -> int:
        return 0


