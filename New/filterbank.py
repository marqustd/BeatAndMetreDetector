import numpy


def filterbank(signal, bandlimits, maxFreq):
    dft = numpy.fft.fft(signal)
    n = dft.size
    nbands = bandlimits.size
    bl = numpy.zeros(nbands)
    br = numpy.zeros(nbands)

    for i in range(1, nbands - 1):
        bl[i] = numpy.floor(bandlimits(i) / maxFreq * n / 2) + 1
        br[i] = numpy.floor(bandlimits(i + 1) / maxFreq * n / 2)

    bl[nbands] = numpy.floor(bandlimits(nbands) / maxFreq * n / 2) + 1
    br[nbands] = numpy.floor(n / 2)

    output = numpy.zeros(n, nbands)

    for i in range(1, nbands):
        output[bl(i): br(i), i] = dft[bl(i): br(i)]
        output[n + 1 - br(i): n + 1 - bl(i), i] = dft[n + 1 - br(i): n + 1 - bl(i)]

    output[1, 1] = 0
    return output
