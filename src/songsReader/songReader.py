from os import name
import audio2numpy
from numpy.core.fromnumeric import shape
import numpy as np


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
    if(len(shape) > 1):
        sample = sample.sum(axis=1)/2

    return sample, samplingFrequency


def read_song_fragment(filename: str, maxDuration: int):
    sample, samplingFrequency = read_song(filename)

    sample = __trim_sample(maxDuration, sample, samplingFrequency)

    return sample, samplingFrequency


def __trim_sample(maxDuration, sample, samplingFrequency):
    if(len(sample)/samplingFrequency > maxDuration):
        maximum = np.max(sample)
        threshold = 0.95
        half = np.floor(len(sample)/2)
        indexes = np.where(sample >= threshold*maximum)[0]
        index = __find_nearest(indexes, half)
        durationLimit = maxDuration*samplingFrequency
        trimmedSample = sample[index:index+durationLimit]

        if(len(trimmedSample)/samplingFrequency >= maxDuration):
            sample = trimmedSample
    return sample


def __find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

if __name__ == '__main__':
    path = '..\\dataset\\genres\\own\\OutKast-Hey-Ya.mp3'
    read_song_fragment(path, 30)
