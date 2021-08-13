from songreader.song import Song

# from tempometredetector.tempodetector import (
#     CombFilterMetreDetector,
#     CombFilterTempoDetector,
#     TempoMetreDetector,
# )
from tempometredetector.metredetector.spectrogram.spectrogram_metre_detector import (
    SpectrogramMetreDetector,
)

spec = SpectrogramMetreDetector()
spec.test_data_songs()
# song = Song("song.wav", bpm=120, metre="4//4")
# tempoDetector = CombFilterTempoDetector()
# metreDetector = CombFilterMetreDetector()
# tempoMetreDetector = TempoMetreDetector(tempoDetector, metreDetector)
# result = tempoMetreDetector.detect_tempo_metre(song)
