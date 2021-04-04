from metre.metreEnum import MetreEnum
from metre.metreDetectorData import MetreDetectorData

class BaseMetreDetector:
    def __str__(self):
        return "BaseMetreDetector"

    def detect_metre(self, data: MetreDetectorData) -> MetreEnum:
        return MetreEnum.UNKNOWN
