import numpy


def diffrect(signal, nbands=6):
    n = len(signal[0])
    output = numpy.zeros([nbands, n])

    for band in range(0, nbands):
        for j in range(5, n):
            d = signal[band, j] - signal[band, j-1]
            if d > 0:
                output[band, j] = d;

    return output
