import tempoMetreDetector as tmd
import song
from tempo import combFilterTempoDetector

from metre import detectMetreConvolve

songs = {
    # song.Song('120', 120, "4/4", 'songs\\test\\120.wav'),
    # song.Song('100', 100, "3/4", 'songs\\test\\100.wav'),
    #
    # song.Song("7-don't_look_back", 89, "4/4", "songs\\rock\\7-don't_look_back.wav"),
    # song.Song("8-i'll_pretend", 140, "4/4", "songs\\rock\\8-i'll_pretend.wav"),
    song.Song("Dave_Brubeck_Quartet_Take_Five", 140, "4/4", "songs\\jazz\\Dave_Brubeck_Quartet_Take_Five.wav"),
    # song.Song("10-at_least_you've_been_told", 130, "4/4", "songs\\rock\\10-at_least_you've_been_told.wav"),
    # song.Song("1-don't_rain_on_my_parade", 160, "4/4", "songs\\rock\\1-don't_rain_on_my_parade.wav"),
    # song.Song("4-goodbye_on_a_beautiful_day", 60, "4/4", "songs\\rock\\4-goodbye_on_a_beautiful_day.wav"),
    # song.Song("5-apartment_a", 115, "4/4", "songs\\rock\\5-apartment_a.wav"),
    # song.Song("12-rotgut", 147, "4/4", "songs\\rock\\12-rotgut.wav"),
    # song.Song("4-buffalo_nights", 147, "4/4", "songs\\rock\\4-buffalo_nights.wav"),
    # song.Song("6-didn't_i", 85, "4/4", "songs\\rock\\6-didn't_i.wav"),
    #
    # song.Song('1-prospects', 126, "4/4", 'songs\\jazz\\1-prospects.wav'),
    #
    # song.Song('7-heavenly_rain', 116, "4/4", 'songs\\metal\\7-heavenly_rain.wav'),
}

tempoDetector = combFilterTempoDetector.CombFilterTempoDetector()
# tempoDetector = convolveTempoDetector.ConvolveTempoDetector()

metreDetector = detectMetreConvolve.DetectMetreConvolve()
# metreDetector = detectMetreNormalized.DetectMetreNormalized()
# metreDetector = detectMetreConvolveNormalized.DetectMetreConvolveNormalized()
# metreDetector = detectMetre.DetectMetre()


file = open("result.txt", 'w')
detector = tmd.TempoMetreDetector(tempoDetector, metreDetector)

for song in songs:
    bpm, metre = detector.detect_tempo_metre(song)
    message = f"Detected in {song.name} song's bpm: {bpm} should be {song.bpm} and metre {metre} should be {song.metre}"
    print(message)
    file.write(message + '\n')

print("End")
file.close()
