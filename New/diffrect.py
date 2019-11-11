import numpy


def diffrect(signal, nbands=6):
    n = signal.size

    output = numpy.zeros(n, nbands)

    for i in range(1, nbands):
        for j in range(5, n):
            d = signal[j, i] - signal[j - 1, i]
            if d > 0:
                output[j, i] = d;

    return output
