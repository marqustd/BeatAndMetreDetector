from tempometredetector.metredetector import MetreEnum, MetreDetectorData


class BaseMetreDetector:
    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self):
        return "BaseMetreDetector"

    def detect_metre(self, data: MetreDetectorData) -> MetreEnum:
        return MetreEnum.UNKNOWN
