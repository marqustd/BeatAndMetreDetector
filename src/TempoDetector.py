import numpy
import WavReader
import filterbank, diffrect, hwindow, timecomb, center
from matplotlib import pyplot as plt


def detect(song, draw_plots=False):
    band_limits = [0, 200, 400, 800, 1600, 3200]

    signal, sample_freq = WavReader.read(song.filepath)

    max_freq = sample_freq
    # Set the number of pulses in the comb filter
    npulses = 10
    sample_length = npulses * max_freq
    seconds = sample_length * 4
    minBpm = 60
    maxBpm = 240

    DrawPlot(draw_plots, signal, f"Song: {song.name}", "Sample/Time", "Amplitude")
    song_length = signal.size

    start = int(numpy.floor(song_length / 2 - seconds / 2))
    stop = int(numpy.floor(song_length / 2 + seconds / 2))
    if start < 0:
        start = 0
    if stop > song_length:
        stop = song_length

    sample = signal[start:stop]

    centred = center.centerSample(sample, sample_length)
    DrawPlot(draw_plots, centred, f"Centred to beat: {song.name}", "Sample/Time", "Amplitude")

    status = f'Filtering song {song.name}...'
    print(status)
    fastFourier = filterbank.filterbank(centred, band_limits, max_freq)

    status = f'Windowing song {song.name}...'
    print(status)
    hanningWindow = hwindow.hwindow(fastFourier, 0.2, band_limits, max_freq)
    if draw_plots:
        plt.plot(hanningWindow[1])
        plt.title("hwindow")
        plt.show()
    status = f'Differentiating song {song.name}...'
    print(status)
    diffrected = diffrect.diffrect(hanningWindow, len(band_limits))
    if draw_plots:
        for band in range(0, len(band_limits)):
            plt.plot(diffrected[band])
            plt.title(f"diffrect[{band}]")
            plt.show()
    status = f'CombFiltering song {song.name}...'
    print(status)

    plot_dictionary = PrepareDict(minBpm, maxBpm)
    first = timecomb.timecomb(signal=diffrected,
                              accuracy=5,
                              minBpm=minBpm,
                              maxBpm=maxBpm,
                              bandlimits=band_limits,
                              maxFreq=max_freq,
                              npulses=npulses,
                              plot_dictionary=plot_dictionary)
    print(f"first: {first}")
    song_bpm = timecomb.timecomb(diffrected, 1, first - 5, first + 5, band_limits, max_freq, npulses, plot_dictionary)

    if draw_plots:
        keys = list(plot_dictionary.keys())
        values = list(plot_dictionary.values())
        plt.plot(keys, values)
        plt.title("Tempo")
        plt.show()
    return song_bpm


def PrepareDict(minBpm, maxBpm):
    dict = {}
    for bpm in range(minBpm, maxBpm):
        dict[bpm] = 0
    return dict


def DrawPlot(isDrawPlots, data, title, xAxis, yAxis, xData= 0):
    if isDrawPlots:
        if xData is 0:
            plt.plot(data)
        else:
            plt.plot(data, xData)
        plt.title(title)
        plt.xlabel(xAxis)
        plt.ylabel(yAxis)
        plt.show()

