from matplotlib import pyplot as plt
import numpy as np


class plotsDrawer:
    isDrawPlots = True

    def prepare_plot_dictionary(this, minBpm, maxBpm):
        dictionary = {}
        for bpm in range(minBpm, maxBpm):
            dictionary[bpm] = 0
        return dictionary

    def draw_plot(this, yData, title, xAxis="Próbki", yAxis="Amplituda", xData=0):
        if this.isDrawPlots:
            if xData is 0:
                plt.plot(yData)
            else:
                plt.plot(yData, xData)
            plt.title(title)
            plt.xlabel(xAxis)
            plt.ylabel(yAxis)
            plt.show()

    def draw_fft_plot(this, yData, plotTitle, samplingFrequency: int):
        if this.isDrawPlots:
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

    def draw_comb_filter_fft_plot(this, yData, plotTitle, samplingFrequency: int):
        if this.isDrawPlots:
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
