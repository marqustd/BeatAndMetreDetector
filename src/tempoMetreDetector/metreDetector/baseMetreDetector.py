from tempoMetreDetector.metreDetector.metreDetectorData import MetreDetectorData
from tempoMetreDetector.metreDetector.metreEnum import MetreEnum


class BaseMetreDetector:
    def __str__(self):
        return "BaseMetreDetector"

    def detect_metre(self, data: MetreDetectorData) -> MetreEnum:
        return MetreEnum.UNKNOWN
