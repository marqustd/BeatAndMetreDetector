import WavReader
import numpy
import filterbank, diffrect, hwindow, timecomb

BANDLIMITS = [0, 200, 400, 800, 1600, 3200]
MAXFREQ = 4096
sampleSize = numpy.floor(2.2 * 2 * MAXFREQ);

song = WavReader.read('test\\1.wav')
song_length = song.size
songSize = len(song)

start = int(numpy.floor(song_length / 2 - sampleSize / 2))
stop = int(numpy.floor(song_length / 2 + sampleSize / 2))

sample = song[start:stop]

status = 'filtering first song...'
print(status)
a = filterbank.filterbank(sample, BANDLIMITS, MAXFREQ)
status = 'windowing first song...'
print(status)
b = hwindow.hwindow(a, 0.2, BANDLIMITS, MAXFREQ)
status = 'differentiating first song...'
print(status)
c = diffrect.diffrect(b, len(BANDLIMITS))
status = 'comb filtering first song...'
print(status)

d = timecomb.timecomb(signal=c, accuracy=10, minBpm=60, maxBpm=240, bandlimits=BANDLIMITS, maxFreq=MAXFREQ)
e = timecomb.timecomb(c, 5, d - 40, d + 40, BANDLIMITS, MAXFREQ)
f = timecomb.timecomb(c, 1, e - 10, e + 10, BANDLIMITS, MAXFREQ)
g = timecomb.timecomb(c, 1, f - 1, f + 1, BANDLIMITS, MAXFREQ)

song_bpm = g
print("Song bpm: ")
print(song_bpm)
