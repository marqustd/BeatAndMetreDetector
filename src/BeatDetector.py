import sys

import TempoMetreDetector as tmd
import numpy as np


bandLimits = [0, 200, 400, 800, 1600, 3200, 6400]
combFilterPulses = 10
minBpm = 60
maxBpm = 240
plotDictionary = {}

def detect(song: tmd.song):
    signal, samplingFrequency = tmd.read_song(song.filepath)
    sample_length = combFilterPulses * samplingFrequency
    seconds = sample_length * 4
    song_length = signal.size
    start = int(np.floor(song_length / 2 - seconds / 2))
    stop = int(np.floor(song_length / 2 + seconds / 2))
    if start < 0:
        start = 0
    if stop > song_length:
        stop = song_length
    sample = signal[start:stop]
    centred = tmd.center_sample_to_beat(sample, sample_length)
    fastFourier = tmd.filterbank(centred, bandLimits, samplingFrequency)
    hanningWindow = tmd.hann(fastFourier, 0.2, bandLimits, samplingFrequency)
    diffrected = tmd.diffrect(hanningWindow, len(bandLimits))
    first = tmd.bpm_comb_filter(diffrected,
                                5,
                                minBpm,
                                maxBpm,
                                bandLimits,
                                samplingFrequency,
                                combFilterPulses,
                                plotDictionary)
    song_bpm = tmd.bpm_comb_filter(diffrected, 1, first - 5, first + 5, bandLimits, samplingFrequency, combFilterPulses,
                                   plotDictionary)
    metre = tmd.detectMetre(diffrected, song_bpm, bandLimits, samplingFrequency, combFilterPulses)

    return song_bpm, metre


songs = {
    # tmd.Song('120', 120, 'songs\\test\\120.wav'),
    # tmd.Song('100', 100, 'songs\\test\\100.wav'),
    #
    # tmd.Song("7-don't_look_back", 89, "songs\\rock\\7-don't_look_back.wav"),
    tmd.Song("8-i'll_pretend", 140, "songs\\rock\\8-i'll_pretend.wav"),
    # tmd.Song("10-at_least_you've_been_told", 130, "songs\\rock\\10-at_least_you've_been_told.wav"),
    # tmd.Song("1-don't_rain_on_my_parade", 160, "songs\\rock\\1-don't_rain_on_my_parade.wav"),
    # tmd.Song("4-goodbye_on_a_beautiful_day", 60, "songs\\rock\\4-goodbye_on_a_beautiful_day.wav"),
    # tmd.Song("5-apartment_a", 115, "songs\\rock\\5-apartment_a.wav"),
    # tmd.Song("12-rotgut", 147, "songs\\rock\\12-rotgut.wav"),
    # tmd.Song("4-buffalo_nights", 147, "songs\\rock\\4-buffalo_nights.wav"),
    # tmd.Song("6-didn't_i", 85, "songs\\rock\\6-didn't_i.wav"),
    #
    # tmd.Song('1-prospects', 126, 'songs\\jazz\\1-prospects.wav'),
    #
    # tmd.Song('7-heavenly_rain', 116, 'songs\\metal\\7-heavenly_rain.wav'),
}

print("This is the name of the script: ", sys.argv[0])
print("Number of arguments: ", len(sys.argv))
print("The arguments are: ", str(sys.argv))

file = open("result.txt", 'w')

for song in songs:
    bpm, metre = detect(song)
    message = f"Detected in {song.name} song's bpm: {bpm} should be {song.bpm}"
    print(message)
    file.write(message+'\n')

print("End")
file.close()

