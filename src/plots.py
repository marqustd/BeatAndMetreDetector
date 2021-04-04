from typing import Dict
from matplotlib import pyplot as plt
import settings
import numpy as np


def preparePlotDictionary(minBpm, maxBpm) -> Dict[int, int]:
    dictionary = {}
    for bpm in range(minBpm, maxBpm):
        dictionary[bpm] = 0
    return dictionary


def drawPlot(yData, title, xAxis="Próbki", yAxis="Amplituda", xData=0) -> None:
    if settings.drawPlots:
        if xData is 0:
            plt.plot(yData)
        else:
            plt.plot(yData, xData)
        plt.title(title)
        plt.xlabel(xAxis)
        plt.ylabel(yAxis)
        plt.show()


def drawFftPlot(yData, plotTitle, samplingFrequency: int) -> None:
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


def drawCombFilterFftPlot(yData, plotTitle, samplingFrequency: int) -> None:
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
