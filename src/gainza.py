# %% Imports
import os
import pandas
import numpy as np
import matplotlib.pyplot as plt
from songreader import read_song_fragment

# %% Import songs list
data = pandas.read_csv(
    "../dataset/genres/genres_tempos.csv", sep=",", names=["path", "tempo", "metre"]
)
data = data[data.metre.notnull()]

# %% Load song sample
song = data.iloc[57]
path = song.path
path = os.path.relpath("../dataset/genres" + path)
# sample, samplingFrequency = songsReader.songReader.read_song(path)
fragmentLength = 30
sample, samplingFrequency = read_song_fragment(path, fragmentLength)

e_time = np.arange(len(sample)) / samplingFrequency


plt.plot(e_time, sample)
plt.title("Audio signal")
plt.ylabel("Waveform")
plt.xlabel("Time [s]")
plt.show()
path


# %% Load music tempo
songTempo = int(song.tempo)
songTempo

# %% Calculate beat duration
beatDurationSec = 60 / songTempo
beatDurationSample = int(beatDurationSec * samplingFrequency)
beatDurationSec

# %% target spectrogram
spectrogram, frequencies, times, im = plt.specgram(
    sample,
    Fs=samplingFrequency,
    NFFT=int(beatDurationSample),
    noverlap=int(beatDurationSample / 32),
    mode="magnitude",
)
plt.title("Spectrogram")
plt.ylabel("Frequency [Hz]")
plt.xlabel("Time [s]")
plt.show()

# # %% mfcc librosa
# audio, samplingFrequency = librosa.load(path=path)
# librosaMfcc = librosa.feature.mfcc(y=audio, sr=samplingFrequency, dct_type=3)

# img = librosa.display.specshow(librosaMfcc, x_axis='time')
# plt.colorbar(img)
# plt.title('MFCC')
# plt.xlabel('Beat')
# plt.ylabel('Feature')
# plt.show()

# # %% Calculate spectrogram
# frequencies, times, spectrogram = signal.spectrogram(
#     sample, samplingFrequency, nperseg=int(beatDurationSample), noverlap=0,)

# %% down spectrogram to 6000 Hz
limitFrequency = 6000
frequenciesLessThan = np.argwhere(frequencies < limitFrequency)
lastIndex = frequenciesLessThan[-1, 0]
frequencies = frequencies[0:lastIndex]
spectrogram = spectrogram[0:lastIndex, :]

# %% calculate percusive component
# window_size = int(beatDurationSample / 4)
# (
#     harmonic,
#     percussive,
#     harmonic_filter,
#     percussive_filter,
# ) = harmonic_percussive_separator.separate_components(spectrogram, window_size)

# # %%
# plt.pcolormesh(times, frequencies, 20 * np.log10(percussive_filter))
# plt.title("Percussive median filter")
# plt.ylabel("Frequency [Hz]")
# plt.xlabel("Time [s]")
# plt.show()

# # %%
# plt.pcolormesh(times, frequencies, 20 * np.log10(harmonic))
# plt.title("Harmonic")
# plt.ylabel("Frequency [Hz]")
# plt.xlabel("Time [s]")
# plt.show()

# # %%
# plt.pcolormesh(times, frequencies, 20 * np.log10(percussive))
# plt.title("Percussive")
# plt.ylabel("Frequency [Hz]")
# plt.xlabel("Time [s]")
# plt.show()

# # %%
# plt.pcolormesh(times, frequencies, 20 * np.log10(harmonic_filter))
# plt.title("Harmonic median filter")
# plt.ylabel("Frequency [Hz]")
# plt.xlabel("Time [s]")
# plt.show()


# %%
# spectrogram = percussive

# %% Calculate AMS
binsAmount = len(times)
asm = np.zeros((binsAmount, binsAmount))


def euclidianDistance(oneBin, secondBin):
    return np.sum(np.square(oneBin - secondBin)), "Euclidian Distance"


def cosineDistance(oneBin, secondBin):
    return (
        1
        - np.sum(np.square(oneBin * secondBin))
        / (np.sqrt(np.sum(np.square(oneBin))) * np.sqrt(sum(np.square(secondBin)))),
        "Cosine Distance",
    )


def kullbackLeibler(oneBin, secondBin):
    return np.sum(oneBin * np.log(oneBin / secondBin)), "Kullback-Leiber"


for x in range(binsAmount):
    thisBin = spectrogram[:, x]
    # for y in range(x, np.min([binsAmount, x+20])):
    for y in range(binsAmount):
        comparedBin = spectrogram[:, y]
        haha = euclidianDistance(thisBin, comparedBin)
        asm[x, y], method = euclidianDistance(thisBin, comparedBin)
        # asm[x, y], method = cosineDistance(thisBin, comparedBin)
        # asm[x, y], method = kullbackLeibler(thisBin, comparedBin)

plt.pcolormesh(asm)
plt.title(f"{method} ASM")
plt.xlabel("Index of frame x")
plt.ylabel("Index of frame y")
plt.show()

# # %% Calculate BMS
# bsm = np.zeros((binsAmount, binsAmount))
# for x in range(1, binsAmount):
#     for y in range(1, binsAmount):
#         bsm[x, y] = asm[x, y] + \
#             np.min([bsm[x-1, y-1], bsm[x-1, y], bsm[x, y-1]])

# plt.pcolormesh(bsm)
# plt.title(f'{method} BSM')
# plt.xlabel('Index of frame x')
# plt.ylabel('Index of frame y')
# plt.show()

# %% Calculate first function d
diagonolasNumber = int(len(asm) / 2)
diagonolasNumber = len(asm)
d = np.zeros(diagonolasNumber)
for i in range(diagonolasNumber):
    d[i] = np.average(np.diag(asm, i))

plt.title("Average value")
plt.xlabel("ASM Diagonal")
plt.plot(d)
plt.xticks(range(0, len(d), 4))
plt.show()

# %% Calculate second function d
for i in range(diagonolasNumber):
    d[i] = -d[i] + np.max(np.abs(d))

plt.title("Diagonal function")
plt.xlabel("ASM Diagonal")
plt.plot(d)
plt.xticks(range(0, len(d), 4))
plt.show()

# %% Calculate Tc index
# metreCandidates = 11
# lt = int(len(bsm)/metreCandidates)
# t = np.zeros(metreCandidates)
# p = np.arange(1, lt, 1)
# for c in range(2, metreCandidates, 1):
#     t[c] = np.sum((d[p*c])/(1-((p-1)/lt)))

metreCandidates = 16
lt = int(len(asm) / metreCandidates)
t = np.zeros(metreCandidates)
for c in range(2, metreCandidates, 1):
    for p in range(1, lt, 1):
        t[c] += (d[p * c]) / (1 - ((p - 1) / lt))

t[0] = 0
t[1] = 0
plt.plot(t)
plt.xlabel("Metre candidate")
plt.ylabel("Tc index")
plt.title(f"Metre prediction for {song.path.split('/')[2]}. Expected: {song.metre}")
plt.xticks(range(0, len(t), 1))
plt.show()

# %% detect metre
metre = np.argmax(t)
metre

# %%
