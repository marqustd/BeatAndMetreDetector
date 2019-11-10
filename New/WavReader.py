import scipy
import numpy as np


class WavReader:

    def read(f, normalized=False):
        """MP3 to numpy array"""
        rate, data = scipy.io.wavfile.read(f)