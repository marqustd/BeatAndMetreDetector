import WavReader
import numpy
import filterbank, diffrect, hwindow, timecomb

BANDLIMITS = [0, 200, 400, 800, 1600, 3200]
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

status = 'filtering first song...'
print(status)
a = filterbank.filterbank(short_sample, BANDLIMITS, MAXFREQ)
status = 'windowing first song...'
print(status)
b = hwindow.hwindow(a, 0.2, BANDLIMITS, MAXFREQ)
status = 'differentiating first song...'
print(status)
c = diffrect.diffrect(b, len(BANDLIMITS))
status = 'comb filtering first song...'
print(status)

d = timecomb.timecomb(c, 2, 60, 240, BANDLIMITS, MAXFREQ)
e = timecomb.timecomb(c, .5, d - 2, d + 2, BANDLIMITS, MAXFREQ)
f = timecomb.timecomb(c, .1, e - .5, e + .5, BANDLIMITS, MAXFREQ)
g = timecomb.timecomb(c, .01, f - .1, f + .1, BANDLIMITS, MAXFREQ)

short_song_bpm = g

status = 'filtering second song...'
print(status)
a = filterbank.filterbank(long_sample, BANDLIMITS, MAXFREQ)
status = 'windowing second song...'
print(status)
b = hwindow.hwindow(a, 0.2, BANDLIMITS, MAXFREQ)
status = 'differentiating second song...'
print(status)
c = diffrect.diffrect(b, len(BANDLIMITS))
status = 'comb filtering second song...'
print(status)

d = timecomb.timecomb(c, 2, 60, 240, BANDLIMITS, MAXFREQ)
e = timecomb.timecomb(c, .5, d - 2, d + 2, BANDLIMITS, MAXFREQ)
f = timecomb.timecomb(c, .1, e - .5, e + .5, BANDLIMITS, MAXFREQ)
g = timecomb.timecomb(c, .01, f - .1, f + .1, BANDLIMITS, MAXFREQ)

long_song_bpm = g
multiple =0
if short_song_bpm > long_song_bpm:
    multiple = short_song_bpm / long_song_bpm
    if abs(short_song_bpm - numpy.floor(multiple) * long_song_bpm) > abs(short_song_bpm - numpy.ceil(multiple) * long_song_bpm):
        new_long_song_bpm = numpy.ceil(multiple) * long_song_bpm
    else:
        new_long_song_bpm = numpy.floor(multiple) * long_song_bpm
    new_short_song_bpm = short_song_bpm
else:
    multiple = long_song_bpm / short_song_bpm;
    if abs(long_song_bpm - numpy.floor(multiple) * short_song_bpm) > abs(long_song_bpm - numpy.ceil(multiple) * short_song_bpm):
        new_short_song_bpm = numpy.ceil(multiple) * short_song_bpm
    else:
        new_short_song_bpm = numpy.floor(multiple) * short_song_bpm
    new_long_song_bpm = long_song_bpm