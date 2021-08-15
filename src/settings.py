from enum import Enum, auto


class MedianFilterEnum(Enum):
    NONE = auto()
    PERCUSIVE = auto()
    HARMONIC = auto()


# comb filters
bandLimits = [0, 200, 400, 800, 1600, 3200, 6400]
combFilterPulses = 8
minBpm = 60
maxBpm = 240

# resampling
resampleSignal = True
resampleRatio = 4

# plots
drawPlots = True
drawTempoFftPlots = True
drawMetreFftPlots = True
drawTempoFilterPlots = True
drawMetreFilterPlots = True
drawSongBpmEnergyPlot = True

# metre
spectrogramLimitFrequency = bandLimits[-1]
medianFilterWindowSize = 201
noverlapRatio = 32
medianFilter = MedianFilterEnum.NONE
