import scipy.io.wavfile
import numpy as np


def read_song(filename):
    sample_freq, data = scipy.io.wavfile.read(filename)
    signal = np.frombuffer(data, np.int16)
    return signal, sample_freq
