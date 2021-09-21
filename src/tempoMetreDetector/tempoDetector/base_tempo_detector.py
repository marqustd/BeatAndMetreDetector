from .tempo_detector_data import TempoDetectorData


class BaseTempoDetector:
    """Base class for detecting song's tempo."""

    def __str__(self):
        return "BaseTempoDetector"

    def __repr__(self) -> str:
        return self.__str__()

    def detect_tempo(self, data: TempoDetectorData) -> int:
        return 0
