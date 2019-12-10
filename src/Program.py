import TempoDetector
import Song

songs = {
    Song.Song('120', 120, 'songs\\test\\120.wav'),
    Song.Song('100', 100, 'songs\\test\\100.wav'),

    Song.Song("7-don't_look_back", 89, "songs\\rock\\7-don't_look_back.wav"),
    Song.Song("8-i'll_pretend", 140, "songs\\rock\\8-i'll_pretend.wav"),
    Song.Song("10-at_least_you've_been_told", 130, "songs\\rock\\10-at_least_you've_been_told.wav"),
    Song.Song("1-don't_rain_on_my_parade", 160, "songs\\rock\\1-don't_rain_on_my_parade.wav"),
    Song.Song("4-goodbye_on_a_beautiful_day", 60, "songs\\rock\\4-goodbye_on_a_beautiful_day.wav"),
    Song.Song("5-apartment_a", 115, "songs\\rock\\5-apartment_a.wav"),
    Song.Song("12-rotgut", 147, "songs\\rock\\12-rotgut.wav"),
    Song.Song("4-buffalo_nights", 147, "songs\\rock\\4-buffalo_nights.wav"),
    Song.Song("6-didn't_i", 85, "songs\\rock\\6-didn't_i.wav"),

    Song.Song('1-prospects', 126, 'songs\\jazz\\1-prospects.wav'),

    Song.Song('7-heavenly_rain', 116, 'songs\\metal\\7-heavenly_rain.wav'),
}

file = open("result.txt", 'w')

for song in songs:
    bpm = TempoDetector.detect(song, False)
    message = f"Detected in {song.name} song's bpm: {bpm} should be {song.bpm}"
    print(message)
    file.write(message+'\n')

print("End")
file.close()
