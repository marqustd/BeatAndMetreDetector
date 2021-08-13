from songreader import song_reader
from tempometredetector.metredetector.spectrogram import asm_calculator, median_filter
import os
import pandas
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def read_data():
    data = pandas.read_csv(
        "../dataset/genres/genres_tempos.mf", sep="\t", names=["path", "tempo", "metre"]
    )
    data = data[data.metre.notnull()]
    return data


def test_data_songs(data):
    good = 0
    bad = 0
    all_songs = len(data)
    for song in data.iloc:
        path = song.path
        path = os.path.relpath("../dataset/genres" + path)
        resul_metre = gainzaFunction.gainzaFunction(path, song.tempo, 4)

        expectedMetre = 0

        if song.metre == "4/4":
            expectedMetre = 4
        elif song.metre == "8/8":
            expectedMetre = 8
        elif song.metre == "5/4":
            expectedMetre = 5

        if resul_metre == expectedMetre or (
            expectedMetre == 4 and (resul_metre == 2 or resul_metre == 8)
        ):
            print(f"Good detection! {expectedMetre}")
            good += 1
        else:
            print(f"Exptected {expectedMetre} but detect {resul_metre}")
            bad += 1

    print(f"All: {all_songs}")
    print(f"Good: {good}")
    print(f"Bad: {bad}")
    print(f"Accuracy: {good/all_songs}")


def get_song_path(data: pandas.DataFrame, song_id: int):
    song = data.iloc[song_id]
    path = song.path
    path = os.path.relpath("../dataset/genres" + path)
    return song, path


data = read_data()
test_data_songs(data)
song, path = get_song_path(data)


def read_song(path):
    fragment_length = 30
    sample, samplingFrequency = song_reader.read_song_fragment(path, fragment_length)

    return sample, samplingFrequency


sample, sampling_frequency = read_song(path)


def plot_song_sample(sample, sampling_frequency):
    e_time = np.arange(len(sample)) / sampling_frequency

    plt.plot(e_time, sample)
    plt.title("Audio signal")
    plt.ylabel("Waveform")
    plt.xlabel("Time [s]")
    plt.show()


plot_song_sample(sample, sampling_frequency)


def get_song_tempo(song):
    songTempo = int(song.tempo)
    return songTempo


songTempo = get_song_tempo(song)


def calculate_beat_duration(samplingFrequency, songTempo):
    beatDurationSec = 60 / songTempo
    beatDurationSample = int(beatDurationSec * samplingFrequency)
    return beatDurationSample


beatDurationSample = calculate_beat_duration(sampling_frequency, songTempo)


spectrogram, frequencies, times = prepare_spectrogram_signal(
    sample, sampling_frequency, beatDurationSample
)


def prepare_spectrogram_signal(sample, samplingFrequency, beatDurationSample):
    frequencies, times, spectrogram = signal.spectrogram(
        sample,
        samplingFrequency,
        nperseg=int(beatDurationSample),
        noverlap=int(beatDurationSample / 32),
        mode="magnitude",
    )

    return spectrogram, frequencies, times


spectrogram, frequencies, times = prepare_spectrogram_signal(
    sample, sampling_frequency, beatDurationSample
)

limitFrequency = 6000


def down_sample_spectrogram(spectrogram, frequencies, times, limitFrequency):
    frequenciesLessThan = np.argwhere(frequencies < limitFrequency)
    lastIndex = frequenciesLessThan[-1, 0]
    frequencies = frequencies[0:lastIndex]
    spectrogram = spectrogram[0:lastIndex, :]

    timesLen = len(times)
    frequenciesLen = len(frequencies)
    return spectrogram


spectrogram = down_sample_spectrogram(spectrogram, frequencies, times, limitFrequency)

windowSize = 201


def calculate_percusive_component(spectrogram, windowSize):
    percusive = median_filter(spectrogram, windowSize, 0)
    spectrogram = percusive
    return spectrogram


spectrogram = calculate_percusive_component(spectrogram, windowSize)
asm = asm_calculator.calculate_asm(
    spectrogram, frequencies, asm_calculator.euclidian_distance
)

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
