# %% Load music sample
import pandas
import numpy as np
from numpy.core.fromnumeric import argmax
from scipy import signal
import songsReader.songReader
import matplotlib.pyplot as plt

song = "song92.wav"
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
plt.specgram(sample, Fs=samplingFrequency, NFFT=beatDurationSample, noverlap=0)
plt.title('Spectrogram')
plt.ylabel("Frequency [Hz]")
plt.xlabel("Time [s]")
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
    # for y in range(x, np.min([binsAmount, x+20])):
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
        bsm[x, y] = asm[x, y] + \
            np.min([bsm[x-1, y-1], bsm[x-1, y], bsm[x, y-1]])

plt.pcolormesh(bsm)
plt.title(f'{method} BSM')
plt.xlabel('Index of frame x')
plt.ylabel('Index of frame y')
plt.show()

# %%
diagonolasNumber = len(bsm)
weight = 1
d = np.zeros(diagonolasNumber)
for i in range(diagonolasNumber):
    d[i] = -np.average(np.diag(bsm, i)) + np.max(np.abs(d))*weight

plt.plot(d)
plt.xticks(range(0, len(d), 4))
plt.show()

# %%
metreCandidates = 11
lt = int(len(bsm)/metreCandidates)
t = np.zeros(metreCandidates)
p = np.arange(1, lt, 1)
for c in range(2, metreCandidates, 1):
    t[c] = np.sum((d[p*c])/(1-((p-1)/lt)))

t[0] = None
t[1] = None
plt.plot(t)
plt.xticks(range(0, len(t), 1))
plt.show()
# %%
import pandas
data = pandas.read_csv('genres_tempos.mf', sep='\t', names=['path', 'tempo', 'metre'])
data = data[data.metre.notnull()]
# %%
