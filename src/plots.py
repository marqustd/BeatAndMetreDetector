from typing import Dict

import matplotlib.pyplot as plt
import numpy as np

import settings


def prepare_plot_dictionary(minBpm, maxBpm) -> Dict[int, int]:
    dictionary = {}
    for bpm in range(minBpm, maxBpm):
        dictionary[bpm] = 0
    return dictionary


def draw_plot(yData, title, xAxis="Próbki", yAxis="Amplituda", xData=0) -> None:
    if settings.drawPlots:
        if xData is 0:
            plt.plot(yData)
        else:
            plt.plot(yData, xData)
        plt.title(title)
        plt.xlabel(xAxis)
        plt.ylabel(yAxis)
        plt.show()


def draw_fft_plot(yData, plotTitle, samplingFrequency: int) -> None:
    if settings.drawPlots:
        length = len(yData)
        h = abs(yData / length)
        h = h[1:int(length / 2 + 1)]
        f = samplingFrequency * ((np.arange(0, int(length / 2))) / length)

        plt.plot(f, h)
        plt.title(plotTitle)
        plt.xlabel("f[Hz]")
        plt.ylabel("|H(f)|")
        plt.xlim(0, 5000)
        plt.show()


def draw_comb_filter_fft_plot(yData, plotTitle, samplingFrequency: int) -> None:
    if settings.drawPlots:
        length = len(yData)
        h = abs(yData / length)
        h = h[1:int(length / 2 + 1)]
        f = samplingFrequency * ((np.arange(0, int(length / 2))) / length)

        plt.plot(f, h)
        plt.title(plotTitle)
        plt.xlabel("f[Hz]")
        plt.ylabel("|H(f)|")
        plt.xlim(0, 10)
        plt.show()


def draw_spectrogram(signal, samplingFrequency: int):
    plt.specgram(signal, Fs=samplingFrequency,
                 NFFT=5000, noverlap=400, cmap='jet_r')
    plt.colorbar()
    plt.show()
