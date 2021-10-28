from scipy import signal
import settings
import numpy as np
import librosa

from tempometredetector.metredetector.metre_detector_data import MetreDetectorData


def get_standard_spectrogram(data: MetreDetectorData):
    beat_duration_samples = __calculate_beat_duration(
        data.sampling_frequency, data.song_tempo
    )

    spectrogram, frequencies, times = __prepare_spectrogram(
        sample_signal=data.signal,
        sampling_frequency=data.sampling_frequency,
        beat_duration_samples=beat_duration_samples,
    )
    spectrogram, frequencies = __limit_spectrogram_frequencies(
        spectrogram=spectrogram,
        frequencies=frequencies,
        limit_frequency=settings.spectrogram_limit_frequency,
    )
    return spectrogram


def get_mffc(data: MetreDetectorData):
    beat_duration_samples = __calculate_beat_duration(
        data.sampling_frequency, data.song_tempo
    )

    audio, sampling_frequency = librosa.load(path=data.path)
    audio = audio[: int(sampling_frequency * settings.fragment_length)]
    librosaMfcc = librosa.feature.mfcc(
        y=audio,
        sr=sampling_frequency,
        dct_type=2,
        n_fft=int(beat_duration_samples / settings.beat_split_ratio),
        hop_length=int(beat_duration_samples / settings.beat_split_ratio),
    )

    return librosaMfcc


def __prepare_spectrogram(sample_signal, sampling_frequency, beat_duration_samples):
    frequencies, times, spectrogram = signal.spectrogram(
        x=sample_signal,
        fs=sampling_frequency,
        nperseg=int(beat_duration_samples / settings.beat_split_ratio),
        noverlap=int(beat_duration_samples / settings.noverlap_ratio),
        mode="magnitude",
    )
    return spectrogram, frequencies, times


def __limit_spectrogram_frequencies(spectrogram, frequencies, limit_frequency):
    frequencies_less_than_limit = np.argwhere(frequencies < limit_frequency)
    last_index = frequencies_less_than_limit[-1, 0]
    frequencies = frequencies[0:last_index]
    spectrogram = spectrogram[0:last_index, :]
    return spectrogram, frequencies


def __calculate_beat_duration(sampling_frequency, songTempo):
    seconds_in_minute = 60
    beat_duration_seconds = seconds_in_minute / songTempo
    beat_duration_samples = int(beat_duration_seconds * sampling_frequency)
    return beat_duration_samples
