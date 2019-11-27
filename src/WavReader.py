import scipy.io.wavfile
import numpy


def read(filename):
    rate, data = scipy.io.wavfile.read(filename)
    signal = numpy.frombuffer(data, numpy.int16)
    return signal
