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

# %% Divide to beat bins

indexes = [0]
for time in np.arange(beatDurationSec, times[-1], beatDurationSec):
    indexes.append(findLastIndexOfLessOrEqual(times, time))
    print(f'time={time} {indexes[-2]}:{indexes[-1]}')

# %% Calculate AMS

# %% Calculate BMS
