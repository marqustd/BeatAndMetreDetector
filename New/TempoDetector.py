import numpy
import filterbank, diffrect, hwindow, timecomb, center
from matplotlib import pyplot as plt


def detect(song, draw_plots=False):
    band_limits = [0, 200, 400, 800, 1600, 3200]
    max_freq = 44100
    # Set the number of pulses in the comb filter
    npulses = 12
    sample_length = (npulses-1) * max_freq + 400
    seconds = sample_length * 3
    minBpm = 60
    maxBpm = 240

    if draw_plots:
        plt.plot(song)
        plt.title("song")
        plt.show()
    song_length = song.size

    start = int(numpy.floor(song_length / 2 - seconds / 2))
    stop = int(numpy.floor(song_length / 2 + seconds / 2))

    sample = song[start:stop]
    if draw_plots:
        plt.plot(sample)
        plt.title("Sample")
        plt.show()

    centred = center.centerSample(sample, sample_length)
    if draw_plots:
        plt.plot(centred)
        plt.title("Centred")
        plt.show()
    status = 'Filtering song...'
    print(status)
    fastFourier = filterbank.filterbank(centred, band_limits, max_freq)

    if draw_plots:
        plt.plot(fastFourier[1])
        plt.title("Filterbank")
        plt.show()

    status = 'Windowing song...'
    print(status)
    hanningWindow = hwindow.hwindow(fastFourier, 0.2, band_limits, max_freq)
    if draw_plots:
        plt.plot(hanningWindow[1])
        plt.title("hwindow")
        plt.show()
    status = 'Differentiating song...'
    print(status)
    diffrected = diffrect.diffrect(hanningWindow, len(band_limits))
    if draw_plots:
        for band in range(0, len(band_limits)):
            plt.plot(diffrected[band])
            plt.title(f"diffrect[{band}]")
            plt.show()
    status = 'CombFiltering song...'
    print(status)

    dict = PrepareDict(minBpm, maxBpm)
    first = timecomb.timecomb(signal=diffrected,
                              accuracy=5,
                              minBpm=minBpm,
                              maxBpm=maxBpm,
                              bandlimits=band_limits,
                              maxFreq=max_freq,
                              npulses=npulses,
                              dict=dict)
    print(f"first: {first}")
    song_bpm = timecomb.timecomb(diffrected, 1, first - 5, first + 5, band_limits, max_freq, npulses, dict)

    if draw_plots:
        keys = list(dict.keys())
        values = list(dict.values())
        plt.plot(keys, values)
        plt.title("Tempo")
        plt.show()
    return song_bpm


def PrepareDict(minBpm, maxBpm):
    dict = {}
    for bpm in range(minBpm, maxBpm):
        dict[bpm] = 0
    return dict
