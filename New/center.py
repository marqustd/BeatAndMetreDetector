import numpy


def centerSample(signal, maxfreq, seconds):
    n = len(signal)
    index = 0

    max = numpy.max(signal)

    for i in range(0, n):
        if signal[i] > max*0.9:
            index = i
            break

    lastindex = seconds * maxfreq
    lastindex += index
    if lastindex > n:
        lastindex = n
    output = signal[index:int(lastindex)]
    return output
