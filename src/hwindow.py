import numpy
from matplotlib import pyplot as plt

#      HWINDOW rectifies a signal, then convolves it with a half Hanning
#      window.
#
#      WINDOWED = HWINDOW(SIG, WINLENGTH, BANDLIMITS, MAXFREQ) takes
#      in a frequecy domain signal as a vector with each column
#      containing a different frequency band. It transforms these
#      into the time domain for rectification, and then back to the
#      frequency domain for multiplication of the FFT of the half
#      Hanning window (Convolution in time domain). The output is a
#      vector with each column holding the time domain signal of a
#      frequency band. BANDLIMITS is a vector of one row in which
#      each element represents the frequency bounds of a band. The
#      final band is bounded by the last element of BANDLIMITS and
#      MAXFREQ. WINLENGTH contains the length of the Hanning window,
#      in time.
#
#     This is the second step of the beat detection sequence.

def hwindow(signal, winLength, bandlimits, maxFreq):
    n = len(signal[0])
    nbands = len(bandlimits)
    hannlen = winLength * 2 * maxFreq
    hann = numpy.zeros(n)
    wave = numpy.zeros([nbands, n], dtype=complex)
    output = numpy.zeros([nbands, n], dtype=complex)
    freq = numpy.zeros([nbands, n], dtype=complex)
    filtered = numpy.zeros([nbands, n], dtype=complex)

    # Create half-Hanning window.
    for a in range(1, int(hannlen)):
        hann[a] = (numpy.cos(a * numpy.pi / hannlen / 2)) ** 2

    # Take IFFT to transfrom to time domain.
    for band in range(0, nbands):
        wave[band] = numpy.real(numpy.fft.ifft(signal[band]))

    # Full - wave rectification in the time domain. And back to frequency with FFT.
    for band in range(0, nbands):
        for j in range(0, n):
            if wave[band, j] < 0:
                wave[band, j] = -wave[band, j]
        freq[band] = numpy.fft.fft(wave[band])

    # Convolving with half - Hanning same as multiplying in frequency.Multiply half - Hanning
    # FFT by signal FFT.Inverse transform to get output in the time domain.
    for band in range(0, nbands):
        filtered[band] = freq[band] * numpy.fft.fft(hann)
        output[band] = numpy.real(numpy.fft.ifft(filtered[band]))

    return output
