from songsreader import Song
from tempometredetector import (
    CombFilterMetreDetector,
    CombFilterTempoDetector,
    TempoMetreDetector,
)

song = Song("song.wav", bpm=120, metre="4//4")
tempoDetector = CombFilterTempoDetector()
metreDetector = CombFilterMetreDetector()
tempoMetreDetector = TempoMetreDetector(tempoDetector, metreDetector)
result = tempoMetreDetector.detect_tempo_metre(song)
