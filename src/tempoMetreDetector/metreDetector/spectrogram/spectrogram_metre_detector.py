from .median_filter import *
from .asm_calculator import *
from songreader.song_reader import read_song_fragment
import os
import pandas
import numpy as np
from scipy import signal
import settings


class SpectrogramMetreDetector:
    def detect_metre(self, path: str, tempo: int, metre: int):
        sample, sampling_frequency = self.__read_song(path)
        if tempo == 0:
            tempo = self.__get_song_tempo(sample)
        beatDurationSample = self.__calculate_beat_duration(sampling_frequency, tempo)

        spectrogram, frequencies, times = self.__prepare_spectrogram_signal(
            sample, sampling_frequency, beatDurationSample
        )
        spectrogram, frequencies = self.__down_sample_spectrogram(
            spectrogram, frequencies, settings.spectrogramLimitFrequency
        )

        spectrogram = self.__apply_median_filter(spectrogram)

        asm = calculate_asm(spectrogram, times, euclidian_distance)
        d = self.__calculate_diagonal_function(asm)
        return self.__detect_metre(asm, d)

    def __apply_median_filter(self, spectrogram):
        if settings.medianFilter == settings.MedianFilterEnum.PERCUSIVE:
            spectrogram = self.__calculate_percusive_component(
                spectrogram, settings.medianFilterWindowSize
            )

        elif settings.medianFilter == settings.MedianFilterEnum.HARMONIC:
            spectrogram = self.__calculate_harmonic_component(
                spectrogram, settings.medianFilterWindowSize
            )

        return spectrogram

    def read_data(self):
        data = pandas.read_csv(
            "../dataset/genres/genres_tempos.csv",
            sep=",",
            names=["path", "tempo", "metre"],
        )
        data = data[data.metre.notnull()]
        return data

    def test_data_songs(self):
        data = self.read_data()
        good = 0
        bad = 0
        all_songs = len(data)
        for song in data.iloc:
            path = song.path
            path = os.path.relpath("../dataset/genres" + path)
            resul_metre = self.detect_metre(path, song.tempo, song.metre)

            expectedMetre = int(song.metre.split("/")[0])

            if resul_metre == expectedMetre or (
                expectedMetre == 4 and (resul_metre == 2 or resul_metre == 8)
            ):
                print(f"Good detection! {expectedMetre} - {song.path}")
                good += 1
            else:
                print(
                    f"Exptected {expectedMetre} but detect {resul_metre} - {song.path}"
                )
                bad += 1

        print(f"All: {all_songs}")
        print(f"Good: {good}")
        print(f"Bad: {bad}")
        print(f"Accuracy: {good/all_songs}")

    def __get_song_path(self, data: pandas.DataFrame, song_id: int):
        song = data.iloc[song_id]
        path = song.path
        path = os.path.relpath("../dataset/genres" + path)
        return song, path

    def __read_song(self, path):
        fragment_length = 30
        sample, samplingFrequency = read_song_fragment(path, fragment_length)
        return sample, samplingFrequency

    def __get_song_tempo(self, song):
        songTempo = int(song.tempo)
        return songTempo

    def __calculate_beat_duration(self, samplingFrequency, songTempo):
        beatDurationSec = 60 / songTempo
        beatDurationSample = int(beatDurationSec * samplingFrequency)
        return beatDurationSample

    def __prepare_spectrogram_signal(
        self, sample, samplingFrequency, beatDurationSample
    ):
        frequencies, times, spectrogram = signal.spectrogram(
            sample,
            samplingFrequency,
            nperseg=int(beatDurationSample),
            noverlap=int(beatDurationSample / settings.noverlapRatio),
            mode="magnitude",
        )
        return spectrogram, frequencies, times

    def __down_sample_spectrogram(self, spectrogram, frequencies, limitFrequency):
        frequenciesLessThan = np.argwhere(frequencies < limitFrequency)
        lastIndex = frequenciesLessThan[-1, 0]
        frequencies = frequencies[0:lastIndex]
        spectrogram = spectrogram[0:lastIndex, :]
        return spectrogram, frequencies

    def __calculate_percusive_component(self, spectrogram, windowSize):
        percusive = median_filter(spectrogram, windowSize, 0)
        spectrogram = percusive
        return spectrogram

    def __calculate_harmonic_component(self, spectrogram, windowSize):
        harmonic = median_filter(spectrogram, 0, windowSize)
        spectrogram = harmonic
        return spectrogram

    def __calculate_diagonal_function(self, asm):
        diagonolasNumber = int(len(asm) / 2)
        diagonolasNumber = len(asm)
        d = np.zeros(diagonolasNumber)
        for i in range(diagonolasNumber):
            d[i] = np.average(np.diag(asm, i))

        for i in range(diagonolasNumber):
            d[i] = -d[i] + np.max(np.abs(d))
        return d

    def __detect_metre(self, asm, d):
        metreCandidates = 16
        lt = int(len(asm) / metreCandidates)
        t = np.zeros(metreCandidates)
        for c in range(2, metreCandidates, 1):
            for p in range(1, lt, 1):
                t[c] += (d[p * c]) / (1 - ((p - 1) / lt))

        t[0] = 0
        t[1] = 0

        metre = np.argmax(t)
        return metre


if __name__ == "__main__":
    detector = SpectrogramMetreDetector()
    detector.test_data_songs()
