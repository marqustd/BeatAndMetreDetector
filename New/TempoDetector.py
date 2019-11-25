import numpy
import filterbank, diffrect, hwindow, timecomb, center
from matplotlib import pyplot as plt


def detect(song, draw_plots=False):
    band_limits = [0, 250, 500, 2000, 4000]
    max_freq = 44100
    # Set the number of pulses in the comb filter
    npulses = 4
    sample_seconds = 2*npulses*max_freq+1
    seconds = 1.5*sample_seconds

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

    centred = center.centerSample(sample, max_freq, sample_seconds)
    if draw_plots:
        plt.plot(centred)
        plt.title("Centred")
        plt.show()
    status = 'filtering first song...'
    print(status)
    fastFourier = filterbank.filterbank(centred, band_limits, max_freq)

    if draw_plots:
        plt.plot(fastFourier[1])
        plt.title("Filterbank")
        plt.show()

    status = 'windowing first song...'
    print(status)
    hanningWindow = hwindow.hwindow(fastFourier, 0.2, band_limits, max_freq)
    if draw_plots:
        plt.plot(hanningWindow[1])
        plt.title("hwindow")
        plt.show()
    status = 'differentiating first song...'
    print(status)
    diffrected = diffrect.diffrect(hanningWindow, len(band_limits))
    if draw_plots:
        plt.plot(diffrected[1])
        plt.title("diffrect")
        plt.show()
    status = 'comb filtering first song...'
    print(status)

    first = timecomb.timecomb(signal=diffrected, accuracy=10, minBpm=60, maxBpm=240, bandlimits=band_limits, maxFreq=max_freq, npulses=npulses)
    print(f"first: {first}")
    second = timecomb.timecomb(diffrected, 5, first - 40, first + 40, band_limits, max_freq, npulses)
    print(f"second: {second}")
    third = timecomb.timecomb(diffrected, 2, second - 10, second + 10, band_limits, max_freq, npulses)
    print(f"third: {third}")
    song_bpm = timecomb.timecomb(diffrected, 1, third-5, third+5, band_limits, max_freq, npulses)

    return song_bpm
