# %% Imports
import os
import librosa
import librosa.display
import pandas
import numpy as np
import matplotlib.pyplot as plt
from common import dataset
from common.dataset import read_dataset
import settings
from songreader import read_song_fragment
from songreader.song_reader import read_song_fragment_from_beginning
from tempometredetector.tempodetector.common import (
    get_comb_filter_fft,
    get_comb_filter_signal,
)

# %%
genres = dataset.read_dataset_genres_fragment(10)
genres

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
sample, sampling_frequency = read_song_fragment(path, settings.fragment_length)

e_time = np.arange(len(sample)) / sampling_frequency


plt.plot(e_time, sample)
plt.title("Audio signal")
plt.ylabel("Waveform")
plt.xlabel("Time [s]")
plt.show()
path

# %% Load music tempo
songTempo = int(song.tempo)
songTempo

# %% librosa tempo
audio, sampling_frequency = librosa.load(path=path)
onset = librosa.onset.onset_strength(audio, sr=sampling_frequency)
librosa_tempo = librosa.beat.tempo(audio, sr=sampling_frequency, onset_envelope=onset)
librosa_tempo

# %%
