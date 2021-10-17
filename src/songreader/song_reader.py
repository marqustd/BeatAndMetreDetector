from os import name
import audio2numpy
from numpy.core.fromnumeric import shape
import numpy as np
import settings


def read_song(filename: str):
    """Reads song and returns it as a numpy array witg sampling frequency

    Args:
        filename (string): Filepath

    Returns:
        numpy array: data
        int: sampling frequency
    """
    sample, samplingFrequency = audio2numpy.open_audio(filename)
    shape = sample.shape
    if len(shape) > 1:
        sample = sample.sum(axis=1) / 2

    return sample, samplingFrequency


def read_song_fragment_from_beginning(filename: str, max_duration: int):
    sample, samplingFrequency = read_song(filename)
    sample = sample[: int(max_duration * samplingFrequency)]
    return sample, samplingFrequency


def read_song_fragment(filename: str, maxDuration: int):
    sample, samplingFrequency = read_song(filename)

    sample = __trim_sample(maxDuration, sample, samplingFrequency)

    return sample, samplingFrequency


def __trim_sample(maxDuration, sample, sampling_frequency):
    if len(sample) / sampling_frequency > maxDuration:
        maximum = np.max(sample)
        threshold = settings.beat_treshold * maximum
        half = np.floor(len(sample) / 2)
        sample = __cut_to_the_nearest_beat_in_half(
            maxDuration, sample, sampling_frequency, half, threshold
        )
    return sample


def __cut_to_the_nearest_beat_in_half(
    max_duration, sample, sampling_frequency, half, threshold
):
    if half < 0:
        return sample[: int(max_duration * sampling_frequency)]

    indexes = np.where(sample >= threshold)[0]
    index = __find_nearest(indexes, half)
    durationLimit = max_duration * sampling_frequency
    trimmedSample = sample[index : index + durationLimit]

    if len(trimmedSample) / sampling_frequency >= max_duration:
        sample = trimmedSample
    else:
        return __cut_to_the_nearest_beat_in_half(
            max_duration,
            sample,
            sampling_frequency,
            half - sampling_frequency * 0.1,
            threshold,
        )
    return sample


def __find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


if __name__ == "__main__":
    path = "..\\dataset\\genres\\own\\OutKast-Hey-Ya.mp3"
    read_song_fragment(path, 30)
