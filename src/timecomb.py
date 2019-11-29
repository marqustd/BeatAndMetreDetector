import numpy
from matplotlib import pyplot as plt


# TIMECOMB finds the tempo of a musical signal, divided into
# frequency bands.
#
#     BPM = TIMECOMB(SIG, ACC, MINBPM, MAXBPM, BANDLIMITS, MAXFREQ)
#     takes in a vector containing a signal, with each band stored
#     in a different column. BANDLIMITS is a vector of one row in
#     which each element represents the frequency bounds of a
#     band. The final band is bounded by the last element of
#     BANDLIMITS and MAXFREQ. The beat resolution is defined in
#     ACC, and the range of beats to test is  defined by MINBPM and
#     MAXBPM.
#
#     Note that timecomb can be recursively called with greater
#     accuracy and a smaller range to speed up computation.
#
#     This is the last step of the beat detection sequence.
def timecomb(signal, accuracy, minBpm, maxBpm, bandlimits, maxFreq, npulses, plot_dictionary):
    n = len(signal[0])
    nbands = len(bandlimits)
    dft = numpy.zeros([nbands, n], dtype=complex)

    if minBpm < 60:
        minBpm = 60

    if maxBpm > 240:
        maxBpm = 240

    # Get signal in frequency domain
    for band in range(0, nbands):
        dft[band] = numpy.fft.fft(signal[band])

    # % Initialize max energy to zero
    maxe = 0
    for bpm in range(minBpm, maxBpm, accuracy):
        # % Initialize energy and filter to zero(s)
        e = 0
        fil = numpy.zeros(n)

        # Calculate the difference between peaks in the filter for a certain tempo
        nstep = numpy.floor(60 / bpm * maxFreq)
        percent_done = 100 * (bpm - minBpm) / (maxBpm - minBpm)
        print(percent_done)


        # Set every nstep samples of the filter to one
        for a in range(0, npulses):
            fil[a * int(nstep) + 1] = 1

        # Get the filter in the frequency domain
        dftfil = numpy.fft.fft(fil)

        # plt.plot(fil)
        # plt.title(f"fil bpm:{bpm} npulses:{npulses}")
        # plt.show()
        #
        # plt.plot(dftfil)
        # plt.title(f"dftfil bpm:{bpm} npulses:{npulses}")
        # plt.show()

        for band in range(0, nbands):
            # plt.plot(signal[band])
            # plt.title(f"signal[{band}]")
            # plt.show()
            # plt.plot(dft[band])
            # plt.title(f"dft[{band}]")
            # plt.show()
            x = (abs(dftfil * dft[band])) ** 2
            e = e + sum(x)

        plot_dictionary[bpm] = e
        # If greater than all previous energies, set current bpm to the bpm of the signal
        if e > maxe:
            sbpm = bpm
            maxe = e

    output = sbpm
    return output