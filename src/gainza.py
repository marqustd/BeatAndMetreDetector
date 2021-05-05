# %% Load music sample
from utilities import findLastIndexOfLessOrEqual
import numpy as np
from scipy import signal
import songsReader.songReader
import matplotlib.pyplot as plt

song = "song.wav"
sample, samplingFrequency = songsReader.songReader.read_song(song)
plt.plot(sample)
plt.show()
sample

# %% Load music tempo
songTempo = 92
songTempo

# %% target spectrogram
plt.specgram(sample, Fs=samplingFrequency, NFFT=1024, noverlap=900)
plt.show()

# %% Calculate spectrogram

frequencies, times, spectrogram = signal.spectrogram(sample, samplingFrequency)

# %% Calculate beat duration
beatDurationSec = 60 / songTempo
beatDurationSec

# %% Calcute time ranges
timesIndexes = [0]
for time in np.arange(beatDurationSec, times[-1], beatDurationSec):
    timesIndexes.append(findLastIndexOfLessOrEqual(times, time))

# %% Divide to beat bins
beats = np.ndarray((len(timesIndexes), 129))  # todo
for i in range(len(timesIndexes)-1):
    timeRange = (spectrogram[:, timesIndexes[i]:timesIndexes[i+1]])
    beat = np.ndarray(129)
    transposed = np.transpose(timeRange)
    for k in range(len(transposed)):
        beat[k] = sum(transposed[k])
    beats[i] = beat


# %% Calculate AMS
# %% Calculate BMS
