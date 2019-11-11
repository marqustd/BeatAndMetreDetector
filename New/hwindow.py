import numpy


def hwindow(signal, winLength, bandlimits, maxFreq):
    n = signal.size
    nbands = bandlimits.size
    hannlen = winLength * 2 * maxFreq
    hann = numpy.zeros(n, 1)
    wave = numpy.zeros(nbands, nbands)
    output = numpy.zeros(nbands, nbands)
    freq = numpy.zeros(nbands, nbands)
    filtered = numpy.zeros(nbands, nbands)

    for a in range(1, hannlen):
        hann[a] = (numpy.cos(a * numpy.pi / hannlen / 2)) ** 2

    for i in range(1, nbands):
        wave[:, i] = numpy.real(numpy.fft.ifft(signal[:, i]))

    for i in range(1, nbands):
        for j in range(1, n):
            if wave[j, i] < 0:
                wave[j, i] = -wave[j, i]
        freq[:, i] = numpy.fft.fft(wave[:, i])

    for i in range(1, nbands):
        filtered[:, i] = freq[:, i] * numpy.fft.fft(hann)
        output[:, i] = numpy.real(numpy.fft.ifft(filtered[:, i]))
    return output
