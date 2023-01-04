from tempometredetector.metredetector.metre_detector_data import MetreDetectorData


class BaseMetreDetector:
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "BaseMetreDetector"

    def detect_metre(self, data: MetreDetectorData):
        return 0
