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
    sample, samplingFrequency, nperseg=beatDurationSample, noverlap=0)

# %% Calculate AMS
binsAmount = len(times)
asm = np.zeros((binsAmount, binsAmount))


def euclidianDistance(oneBin, secondBin):
    return np.sum(np.square(oneBin-secondBin)), 'Euclidian Distance'


def cosineDistance(oneBin, secondBin):
    return 1 - np.sum(np.square(oneBin*secondBin))/(np.sqrt(np.sum(np.square(oneBin)))*np.sqrt(sum(np.square(secondBin)))), 'Cosine Distance'


def kullbackLeibler(oneBin, secondBin):
    return np.sum(oneBin*np.log(oneBin/secondBin)), 'Kullback-Leiber'


for x in range(binsAmount):
    thisBin = spectrogram[:, x]
    # for y in range(x, min(binsAmount, x+10)):
    for y in range(binsAmount):
        comparedBin = spectrogram[:, y]
        asm[x, y], method = euclidianDistance(thisBin, comparedBin)
        # asm[x, y], method = cosineDistance(thisBin, comparedBin)
        # asm[x, y], method = kullbackLeibler(thisBin, comparedBin)

plt.pcolormesh(asm)
plt.title(f'{method} ASM')
plt.xlabel('Index of frame x')
plt.ylabel('Index of frame y')
plt.show()

# %% Calculate BMS
bsm = np.zeros((binsAmount, binsAmount))
for x in range(1, binsAmount):
    for y in range(1, binsAmount):
        bsm[x, y] = asm[x, y] + min(bsm[x-1, y-1], bsm[x-1, y], bsm[x, y-1])
        
plt.pcolormesh(bsm)
plt.title(f'{method} BSM')
plt.xlabel('Index of frame x')
plt.ylabel('Index of frame y')
plt.show()

# %%
