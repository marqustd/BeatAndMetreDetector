import WavReader
import numpy
import TempoDetector

BANDLIMITS = [0, 200, 400, 800, 1600, 3200]
MAXFREQ = 44100
sampleSize = numpy.floor(2.2 * MAXFREQ)
drawPlots = False

song = WavReader.read('pop\\1.wav')

song_bpm = TempoDetector.detect(song, False)
print("Song bpm: ")
print(song_bpm)
