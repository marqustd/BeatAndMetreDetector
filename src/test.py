import tempoMetreDetector as tmd
import song
from tempo import combFilterTempoDetector, convolveTempoDetector

from metre import convolveMetreDetector, convolveNormalizedMetreDetector, combFilterMetreDetector, \
    combFilterNormalizedMetreDetector, correlateNormalizedMetreDetector

songs = {
    song.Song('songs\\test\\120.wav', '120', 120, "4/4"),
    song.Song('songs\\test\\100.wav', '100', 100, "3/4"),

    # song.Song("songs\\rock\\7-don't_look_back.wav", "7-don't_look_back", 89, "4/4"),
    # song.Song("songs\\rock\\8-i'll_pretend.wav", "8-i'll_pretend", 140, "4/4"),
    # song.Song("songs\\jazz\\Dave_Brubeck_Quartet_Take_Five.wav", "Dave_Brubeck_Quartet_Take_Five", 140, "5/4"),
    # song.Song("songs\\rock\\10-at_least_you've_been_told.wav", "10-at_least_you've_been_told", 130, "4/4"),
    # song.Song("songs\\rock\\1-don't_rain_on_my_parade.wav", "1-don't_rain_on_my_parade", 160, "4/4"),
    # song.Song("songs\\rock\\4-goodbye_on_a_beautiful_day.wav", "4-goodbye_on_a_beautiful_day", 60, "4/4"),
    # song.Song("songs\\rock\\5-apartment_a.wav", "5-apartment_a", 115, "4/4"),
    # song.Song("songs\\rock\\12-rotgut.wav", "12-rotgut", 147, "4/4"),
    # song.Song("songs\\rock\\4-buffalo_nights.wav", "4-buffalo_nights", 147, "4/4"),
    # song.Song("songs\\rock\\6-didn't_i.wav", "6-didn't_i", 85, "4/4"),
    #
    # song.Song('songs\\jazz\\1-prospects.wav', '1-prospects', 126, "4/4"),
    #
    # song.Song('songs\\metal\\7-heavenly_rain.wav', '7-heavenly_rain', 116, "4/4"),
}

tempoDetector = combFilterTempoDetector.CombFilterTempoDetector()
# tempoDetector = convolveTempoDetector.ConvolveTempoDetector()

# metreDetector = convolveMetreDetector.ConvolveMetreDetector()
# metreDetector = convolveNormalizedMetreDetector.ConvolveNormalizedMetreDetector()
# metreDetector = combFilterMetreDetector.CombFilterMetreDetector()
# metreDetector = combFilterNormalizedMetreDetector.CombFilterNormalizedMetreDetector()
metreDetector = correlateNormalizedMetreDetector.CorrelateNormalizedMetreDetector()

file = open("result.txt", 'w')
detector = tmd.TempoMetreDetector(tempoDetector, metreDetector)

for song in songs:
    bpm, metre, time = detector.detect_tempo_metre(song)
    message = f"Detected in {song.name} song's bpm: {bpm} should be {song.bpm} and metre {metre} should be {song.metre}"
    print(message)
    file.write(message + '\n')

print("End")
file.close()
