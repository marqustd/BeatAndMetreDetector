class BaseMetreDetector:
    def __str__(self):
        return "BaseMetreDetector"

    def detect_metre(self, signal, tempo: int, bandlimits, maxFreq, npulses):
        return "metre"
