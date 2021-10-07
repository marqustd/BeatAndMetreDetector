from tempometredetector import tempo_metre_detector
from tempometredetector.metredetector.spectrogram.spectrogram_metre_detector import (
    SpectrogramMetreDetector,
)


tempo_metre_detector = tempo_metre_detector.TempoMetreDetector(
    tempo_detector=None, metre_detector=SpectrogramMetreDetector
)

tempo_metre_detector.detect_tempo
