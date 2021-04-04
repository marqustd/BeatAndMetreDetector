import scipy.io.wavfile
import numpy as np


def read_song(filename: str):
    """Reads song and returns it as a numpy array witg sampling frequency

    Args:
        filename (string): Filepath

    Returns:
        numpy array: data
        int: sampling frequency
    """
    sample_freq, data = scipy.io.wavfile.read(filename)
    signal = np.frombuffer(data, np.int16)
    return signal, sample_freq
