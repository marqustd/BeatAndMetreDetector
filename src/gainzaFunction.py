# %% Imports
import os
import pandas
import numpy as np
from numpy.core.fromnumeric import argmax
from scipy import signal
import songsReader.songReader
import matplotlib.pyplot as plt


def gainzaFunction(path: str, songTempo: int, metre: int):
    sample, samplingFrequency = songsReader.songReader.read_song(path)

    if(len(sample)/samplingFrequency > 30):
        durationLimit = 30*samplingFrequency
        sample = sample[0:durationLimit]

    beatDurationSec = 60 / songTempo
    beatDurationSample = int(beatDurationSec * samplingFrequency)
    beatDurationSec

    frequencies, times, spectrogram = signal.spectrogram(
        sample, samplingFrequency, nperseg=int(beatDurationSample), noverlap=0,)

    frequenciesLessThan = np.argwhere(frequencies < 8000)
    lastIndex = frequenciesLessThan[-1, 0]
    frequencies = frequencies[0:lastIndex]
    spectrogram = spectrogram[0:lastIndex, :]

    binsAmount = len(times)
    asm = np.zeros((binsAmount, binsAmount))

    for x in range(binsAmount):
        thisBin = spectrogram[:, x]
        # for y in range(x, np.min([binsAmount, x+20])):
        for y in range(binsAmount):
            comparedBin = spectrogram[:, y]
            asm[x, y], method = euclidianDistance(thisBin, comparedBin)
            # asm[x, y], method = cosineDistance(thisBin, comparedBin)
            # asm[x, y], method = kullbackLeibler(thisBin, comparedBin)

    diagonolasNumber = int(len(asm)/2)
    diagonolasNumber = len(asm)
    d = np.zeros(diagonolasNumber)
    for i in range(diagonolasNumber):
        d[i] = np.average(np.diag(asm, i))

    for i in range(diagonolasNumber):
        d[i] = -d[i] + np.max(np.abs(d))

    metreCandidates = 11
    lt = int(len(asm)/metreCandidates)
    t = np.zeros(metreCandidates)
    for c in range(2, metreCandidates, 1):
        for p in range(1, lt, 1):
            t[c] += ((d[p*c])/(1-((p-1)/lt)))

    t[0] = 0
    t[1] = 0
    metre = np.argmax(t)
    
    return metre


def euclidianDistance(oneBin, secondBin):
    return np.sum(np.square(oneBin-secondBin)), 'Euclidian Distance'


def cosineDistance(oneBin, secondBin):
    return 1 - np.sum(np.square(oneBin*secondBin))/(np.sqrt(np.sum(np.square(oneBin)))*np.sqrt(sum(np.square(secondBin)))), 'Cosine Distance'


def kullbackLeibler(oneBin, secondBin):
    return np.sum(oneBin*np.log(oneBin/secondBin)), 'Kullback-Leiber'
# %%
