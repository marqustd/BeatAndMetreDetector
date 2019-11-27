import numpy


# FILTERBANK divides a time domain signal into individual frequency bands.
#
#      FREQBANDS = FILTERBANK(SIG, BANDLIMITS, MAXFREQ) takes in a
#      time domain signal stored in a column vector, and outputs a
#      vector of the signal in the frequency domain, with each
#      column representing a different band. BANDLIMITS is a vector
#      of one row in which each element represents the frequency
#      bounds of a band. The final band is bounded by the last
#      element of BANDLIMITS and  MAXFREQ.
#
#      This is the first step of the beat detection sequence.

def filterbank(signal, bandlimits, maxFreq):
    dft = numpy.fft.fft(signal)
    n = len(dft)
    nbands = len(bandlimits)
    bl = numpy.zeros(nbands, int)
    br = numpy.zeros(nbands, int)

    #   % Bring band scale from Hz to the points in our vectors
    for band in range(0, nbands - 1):
        bl[band] = numpy.floor(bandlimits[band] / maxFreq * n / 2) + 1
        br[band] = numpy.floor(bandlimits[band + 1] / maxFreq * n / 2)

    bl[0] = 0
    bl[nbands - 1] = numpy.floor(bandlimits[nbands - 1] / maxFreq * n / 2) + 1
    br[nbands - 1] = numpy.floor(n / 2)

    output = numpy.zeros([nbands, n], dtype=complex)

    # Create the frequency bands and put them in the vector output.
    for band in range(0, nbands):
        for hz in range(bl[band], br[band]):
            output[band, hz] = dft[hz]
        for hz in range(n - br[band], n - bl[band]):
            output[band, hz] = dft[hz]
        # output[int(bl[band]): int(br[band])][band] = dft[int(bl[band]): int(br[band])]
        # output[n + 1 - br[band]: n + 1 - bl[band], band] = dft[n + 1 - br[band]: n + 1 - bl[band]]

    output[1, 1] = 0
    return output
