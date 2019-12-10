import scipy.io.wavfile
import numpy


def read(filename):
    sample_freq, data = scipy.io.wavfile.read(filename)
    signal = numpy.frombuffer(data, numpy.int16)
    return signal, sample_freq
