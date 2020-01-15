from matplotlib import pyplot as plt
import numpy as np


def prepare_plot_dictionary(minBpm, maxBpm):
    dictionary = {}
    for bpm in range(minBpm, maxBpm):
        dictionary[bpm] = 0
    return dictionary


def draw_plot(is_draw_plots: bool, yData, title, xAxis="Próbki", yAxis="Amplituda", xData=0):
    if is_draw_plots:
        if xData is 0:
            plt.plot(yData)
        else:
            plt.plot(yData, xData)
        plt.title(title)
        plt.xlabel(xAxis)
        plt.ylabel(yAxis)
        plt.show()


def draw_fft_plot(drawPlots: bool, yData, plotTitle, samplingFrequency: int):
    if drawPlots:
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


def draw_comb_filter_fft_plot(is_draw_plots: bool, yData, plotTitle, samplingFrequency: int):
    if is_draw_plots:
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
