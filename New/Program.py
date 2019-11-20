import WavReader
import numpy
import filterbank, diffrect, hwindow, timecomb
from matplotlib import pyplot as plt

BANDLIMITS = [0, 200, 400, 800, 1600, 3200]
MAXFREQ = 44100
sampleSize = numpy.floor(2.2 * MAXFREQ);

song = WavReader.read('pop\\1.wav')
plt.plot(song)
plt.title("song")
plt.show()
song_length = song.size
songSize = len(song)

start = int(numpy.floor(song_length / 2 - sampleSize / 2))
stop = int(numpy.floor(song_length / 2 + sampleSize / 2))

sample = song[start:stop]
plt.plot(sample)
plt.title("Sample")
plt.show()
status = 'filtering first song...'
print(status)
a = filterbank.filterbank(sample, BANDLIMITS, MAXFREQ)
plt.plot(a[1])
plt.title("Filterbank")
plt.show()
status = 'windowing first song...'
print(status)
b = hwindow.hwindow(a, 0.2, BANDLIMITS, MAXFREQ)
plt.plot(b[1])
plt.title("hwindow")
plt.show()
status = 'differentiating first song...'
print(status)
c = diffrect.diffrect(b, len(BANDLIMITS))
plt.plot(c[1])
plt.title("diffrect")
plt.show()
status = 'comb filtering first song...'
print(status)

d = timecomb.timecomb(signal=c, accuracy=10, minBpm=60, maxBpm=240, bandlimits=BANDLIMITS, maxFreq=MAXFREQ)
print("first: ")
print(d)
e = timecomb.timecomb(c, 5, d - 40, d + 40, BANDLIMITS, MAXFREQ)
print("second: ")
print(e)
f = timecomb.timecomb(c, 1, e - 10, e + 10, BANDLIMITS, MAXFREQ)
print("third: ")
print(f)
g = timecomb.timecomb(c, 1, f - 1, f + 1, BANDLIMITS, MAXFREQ)

song_bpm = g
print("Song bpm: ")
print(song_bpm)
