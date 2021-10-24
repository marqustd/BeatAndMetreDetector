# %% Imports
import os
import librosa
import librosa.display
import pandas
import numpy as np
import matplotlib.pyplot as plt
from common.dataset import read_dataset
import settings
from songreader import read_song_fragment
from songreader.song_reader import read_song_fragment_from_beginning

# %% Import songs list
data = pandas.read_csv(
    "../dataset/genres/genres_tempos.csv", sep=",", names=["path", "tempo", "metre"]
)

data

# %% Load song sample
song = data.iloc[1]
path = song.path
path = os.path.relpath("../dataset/genres" + path)

# sample, samplingFrequency = songsReader.songReader.read_song(path)
sample, samplingFrequency = read_song_fragment(path, settings.fragment_length)

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
beatDurationSample = int(beatDurationSec * samplingFrequency) / 8
beatDurationSec / 8

# %% target spectrogram
spectrogram, frequencies, times, im = plt.specgram(
    sample,
    Fs=samplingFrequency,
    NFFT=int(beatDurationSample / settings.beat_split_ratio),
    noverlap=int(beatDurationSample / settings.noverlap_ratio),
    mode="magnitude",
)
plt.title("Spectrogram")
plt.ylabel("Frequency [Hz]")
plt.xlabel("Time [s]")
plt.show()

# %% mfcc librosa
audio, samplingFrequency = librosa.load(path=path)
audio = audio[: int(samplingFrequency * settings.fragment_length)]

librosaMfcc = librosa.feature.mfcc(
    y=audio,
    sr=samplingFrequency,
    dct_type=2,
    n_fft=int(beatDurationSample / settings.beat_split_ratio),
    hop_length=int(beatDurationSample / settings.beat_split_ratio),
)

img = librosa.display.specshow(librosaMfcc)
plt.colorbar(img)
plt.title("MFCC")
plt.xlabel("Beat")
plt.ylabel("Feature")
plt.show()

# # %% Calculate spectrogram
# frequencies, times, spectrogram = signal.spectrogram(
#     sample, samplingFrequency, nperseg=int(beatDurationSample), noverlap=0,)

# %% down spectrogram to limit Hz
frequenciesLessThan = np.argwhere(frequencies < settings.spectrogram_limit_frequency)
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
spectrogram = librosaMfcc
binsAmount = len(times)
asm = np.zeros((binsAmount, binsAmount))

for x in range(binsAmount):
    thisBin = spectrogram[:, x]
    # for y in range(x, np.min([binsAmount, x+20])):
    for y in range(binsAmount):
        comparedBin = spectrogram[:, y]
        asm[x, y] = settings.method(thisBin, comparedBin)

plt.pcolormesh(asm)
plt.title(f"{settings.method} ASM")
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
diagonolasNumber = len(asm)
d = np.zeros(diagonolasNumber)
for g in range(diagonolasNumber):
    d[g] = np.average(np.diag(asm, g))

plt.title("Average value")
plt.xlabel("ASM Diagonal")
plt.plot(d)
plt.xticks(range(0, len(d), 4))
plt.show()

# %% Calculate second function d
for g in range(len(d)):
    d[g] = -d[g] + np.max(np.abs(d))

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

metreCandidates = settings.metre_candidates
lt = int(len(d) / metreCandidates)
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
