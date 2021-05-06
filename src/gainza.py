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

# %% Calculate beat duration
beatDurationSec = 60 / songTempo
beatDurationSample = int(beatDurationSec * samplingFrequency)
beatDurationSec

# %% target spectrogram
plt.specgram(sample, Fs=samplingFrequency, NFFT=beatDurationSample)
plt.show()

# %% Calculate spectrogram
frequencies, times, spectrogram = signal.spectrogram(
    sample, samplingFrequency, nperseg=beatDurationSample)

# %% Calculate AMS
binsAmount = len(times)
ams = np.ndarray((binsAmount, binsAmount))

for x in range(binsAmount):
    thisbin = spectrogram[:, x]
    for y in range(binsAmount):
        comparedBin = spectrogram[:, y]
        ams[y, x] = sum(thisbin-comparedBin)

#%%        
plt.pcolormesh(ams)
plt.show()

# %% Calculate BMS
