import numpy


def timecomb(signal, accuracy, minBpm, maxBpm, bandlimits, maxFreq):
    n = len(signal[0])
    nbands = len(bandlimits)
    npulses = 3
    dft = numpy.zeros([nbands, n])

    for band in range(0, nbands):
        dft[band, :] = numpy.fft.fft(signal[band, :])

    maxe = 0
    for bpm in range(minBpm, maxBpm, accuracy):
        e = 0
        fil = numpy.zeros(n)
        nstep = numpy.floor(120 / bpm * maxFreq)
        percent_done = 100 * (bpm - minBpm) / (maxBpm - minBpm)
        print(percent_done)

        for a in range(0, npulses - 1):
            fil[a * int(nstep) + 1] = 1

        dftfil = numpy.fft.fft(fil)

        for band in range(0, nbands):
            x = (abs(dftfil * dft[band, :])) ** 2
            e = e + sum(x)

        if e > maxe:
            sbpm = bpm
            maxe = e

    output = sbpm
    return output
