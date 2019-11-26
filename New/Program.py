import WavReader
import TempoDetector
import Song

songs = {
    # Song.Song('120', 120, 'songs\\test\\120.wav'),
    # Song.Song('100', 100, 'songs\\test\\100.wav'),
    # Song.Song('1-propinan_de_melyor', 115, 'songs\\classical\\1-propinan_de_melyor.wav'),
    # Song.Song('18-dolce_amoroso_focho', 140, 'songs\\classical\\18-dolce_amoroso_focho.wav'),
    # Song.Song('1-soul_print', 130, 'songs\\metal\\1-soul_print.wav'),
    # Song.Song('11-divine_toy', 160, 'songs\\metal\\11-divine_toy.wav'),
    # Song.Song('6-trugnale_marko', 150, 'songs\\world\\6-trugnale_marko.wav'),
    # Song.Song('8-daldalar_tamzara', 170, 'songs\\world\\8-daldalar_tamzara.wav'),
    # Song.Song('1-fizz', 158, 'songs\\rock\\1-fizz.wav'),
    # Song.Song('3-wnqd', 123, 'songs\\rock\\3-wnqd.wav'),
    # Song.Song('4-set_fire_to_the_city', 67, 'songs\\rock\\4-set_fire_to_the_city.wav'),
    # Song.Song("6-didn't_i", 85, "songs\\rock\\6-didn't_i.wav"),
    # Song.Song('3-erase', 119, 'songs\\pop\\3-erase.wav'),
    Song.Song('5-river', 110, 'songs\\pop\\5-river.wav'),
}

file = open("result.txt", 'w')

for song in songs:
    signal = WavReader.read(song.filepath)
    bpm = TempoDetector.detect(signal, True)
    message = f"Detected in {song.name} song's bpm: {bpm} should be {song.bpm}"
    print(message)
    file.write(message+'\n')

print("End")
file.close()
