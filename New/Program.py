import WavReader
import numpy

BANDLIMITS = [0, 200, 400, 800, 1600, 3200, 6400, 12800]
MAXFREQ = 4096
sampleSize = numpy.floor(2.2*2*MAXFREQ);

song1 = WavReader.read('rock\\1.wav')
song2 = WavReader.read('rock\\2.wav')

if song1.size < song2.size:
    short_song = song1
    long_song = song2
    short_length = song1.size
else:
    short_song = song2
    long_song = song1
    short_length = song2.size

start = int(numpy.floor(short_length/2 - sampleSize/2))
stop = int(numpy.floor(short_length/2 + sampleSize/2))

short_sample = short_song[start:stop]
long_sample = long_song[start:stop]
