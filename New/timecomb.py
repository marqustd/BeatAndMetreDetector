import numpy


def timecomb(signal, accuracy, minBpm, maxBpm, bandlimits, maxFreq):
    n = signal.size
    nbands = bandlimits.size
    npulses = 3
    dft = numpy.zeros([nbands, nbands])

    for i in range(1, nbands):
        dft[:, i] = numpy.fft.fft(signal[:, i])

    maxe = 0
    for bpm in range(minBpm, maxBpm, accuracy):
        e = 0
        fil = numpy.zeros(n, 1)
        nstep = numpy.floor(120 / bpm * maxFreq)
        percent_done = 100 * (bpm - minBpm) / (maxBpm - minBpm)
        print(percent_done)

        for a in range(0, npulses - 1):
            fil[a * nstep + 1] = 1

        dftfil = numpy.fft.fft(fil)

        for i in range(1, nbands):
            x = (abs(dftfil * dft[:, i])) ** 2
            e = e + sum(x)

        if e > maxe:
            sbpm = bpm
        maxe = e

    output = sbpm
    return output
