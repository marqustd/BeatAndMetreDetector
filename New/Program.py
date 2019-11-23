import WavReader
import numpy
import TempoDetector
import Song

BANDLIMITS = [0, 200, 400, 800, 1600, 3200]
MAXFREQ = 44100
sampleSize = numpy.floor(2.2 * MAXFREQ)
drawPlots = False

songs = {
    Song.Song('120', 120, 'songs\\test\\120.wav'),
    Song.Song('100', 100, 'songs\\test\\100.wav'),
    Song.Song('1-propinan_de_melyor', 115, 'songs\\classical\\1-propinan_de_melyor.wav'),
    Song.Song('18-dolce_amoroso_focho', 140, 'songs\\classical\\18-dolce_amoroso_focho.wav'),
    Song.Song('1-soul_print', 130, 'songs\\metal\\1-soul_print.wav'),
    Song.Song('11-divine_toy', 160, 'songs\\metal\\11-divine_toy.wav'),
    Song.Song('6-trugnale_marko', 150, 'songs\\world\\6-trugnale_marko.wav'),
    Song.Song('8-daldalar_tamzara', 170, 'songs\\world\\8-daldalar_tamzara.wav'),
}

for song in songs:
    signal = WavReader.read(song.filepath)
    bpm = TempoDetector.detect(signal, False)
    print(f"Detected in {song.name} song's bpm: {bpm} should be {song.bpm}")
