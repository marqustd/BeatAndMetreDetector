#!/usr/bin/python

import scipy.io.wavfile, numpy, sys, subprocess


# Some abstractions for computation
def sumsquared(arr):
    sum = 0
    for i in arr:
        sum = sum + (i[0] * i[0]) + (i[1] * i[1])

    return sum


#if sys.argv.__len__() < 2:
#    print('USAGE: wavdsp <wavfile>')
#    sys.exit(1)

numpy.set_printoptions(threshold=1)
#rate, data = scipy.io.wavfile.read(sys.argv[1])
rate, data = scipy.io.wavfile.read('C:\\git\\BeatAndMetreEstimator\\New\\ChillingMusic.wav')


# Beat detection algorithm begin
# the algorithm has been implemented as per GameDev Article
# Initialisation
data_len = data.__len__()
idx = 0
hist_last = 44032
instant_energy = 0
local_energy = 0
le_multi = 0.023219955  # Local energy multiplier ~ 1024/44100

# Play the song
#p = subprocess.Popen(['audacious', 'C:\\git\\BeatAndMetreEstimator\\New\\ChillingMusic.wav'])

while idx < data_len - 48000:
    dat = data[idx:idx + 1024]
    history = data[idx:hist_last]
    instant_energy = sumsquared(dat)
    local_energy = le_multi * sumsquared(history)
    print(instant_energy, local_energy)
    if instant_energy > (local_energy * 1.3):
        print('Beat')

    idx = idx + 1024
    hist_last = hist_last + 1024  # Right shift history buffer

p.terminate()
