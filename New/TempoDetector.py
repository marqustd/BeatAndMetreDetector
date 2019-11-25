import numpy
import filterbank, diffrect, hwindow, timecomb
from matplotlib import pyplot as plt


def detect(song, drawPlots=False):
    BANDLIMITS = [0, 250, 500, 2000, 4000]
    MAXFREQ = 44100
    sampleSize = numpy.floor(2.2 * MAXFREQ)

    if drawPlots:
        plt.plot(song)
        plt.title("song")
        plt.show()
    song_length = song.size

    start = int(numpy.floor(song_length / 2 - sampleSize / 2))
    stop = int(numpy.floor(song_length / 2 + sampleSize / 2))

    sample = song[start:stop]
    if drawPlots:
        plt.plot(sample)
        plt.title("Sample")
        plt.show()
    status = 'filtering first song...'
    print(status)
    fastFourier = filterbank.filterbank(sample, BANDLIMITS, MAXFREQ)
    if drawPlots:
        plt.plot(fastFourier[1])
        plt.title("Filterbank")
        plt.show()
    status = 'windowing first song...'
    print(status)
    hanningWindow = hwindow.hwindow(fastFourier, 0.2, BANDLIMITS, MAXFREQ)
    if drawPlots:
        plt.plot(hanningWindow[1])
        plt.title("hwindow")
        plt.show()
    status = 'differentiating first song...'
    print(status)
    diffrected = diffrect.diffrect(hanningWindow, len(BANDLIMITS))
    if drawPlots:
        plt.plot(diffrected[1])
        plt.title("diffrect")
        plt.show()
    status = 'comb filtering first song...'
    print(status)

    first = timecomb.timecomb(signal=diffrected, accuracy=10, minBpm=60, maxBpm=240, bandlimits=BANDLIMITS, maxFreq=MAXFREQ)
    print(f"first: {first}")
    second = timecomb.timecomb(diffrected, 5, first - 40, first + 40, BANDLIMITS, MAXFREQ)
    print(f"second: {second}")
    third = timecomb.timecomb(diffrected, 2, second - 10, second + 10, BANDLIMITS, MAXFREQ)
    print(f"third: {third}")
    song_bpm = timecomb.timecomb(diffrected, 1, third-5, third+5, BANDLIMITS, MAXFREQ)

    return song_bpm
