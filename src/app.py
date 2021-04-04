from songsReader.song import Song
from tempoMetreDetector.metreDetector.combFilterMetreDetector import \
    CombFilterMetreDetector
from tempoMetreDetector.tempoDetector.combFilterTempoDetector import \
    CombFilterTempoDetector
from tempoMetreDetector.tempoMetreDetector import TempoMetreDetector

song = Song("song.wav", bpm=120, metre="4//4")
tempoDetector = CombFilterTempoDetector()
metreDetector = CombFilterMetreDetector()
tempoMetreDetector = TempoMetreDetector(tempoDetector, metreDetector)
result = tempoMetreDetector.detect_tempo_metre(song)
