import common
import settings
import tempoMetreDetector as tmd
from tests import songs, testCase


def launch_test(case: testCase.TestCase):
    settings.resampleSignal = case.resampleSignal
    settings.combFilterPulses = case.combFilterPulses
    settings.resampleRatio = case.resampleRatio
    tempoDetector = case.tempoDetector
    metreDetector = case.metreDetector

    filename = common.prepare_settings_string_filename(tempoDetector, metreDetector)
    file = open("..\\results\\" + filename + ".csv", 'w')
    logic = tmd.TempoMetreDetector(tempoDetector, metreDetector)

    string = common.prepare_settings_string(tempoDetector, metreDetector)
    print(string)
    file.write(string)
    print()
    string = "Song;Detected BPM;Real BPM;Detected metre;Real metre;Time"
    print(string)
    file.write(string + '\n')
    for song in songs.songs:
        bpm, metre, time = logic.detect_tempo_metre(song)
        message = f"{song.name};{bpm};{song.bpm};{metre};{song.metre};{time};"
        print(message)
        file.write(message + '\n')

    print("End")
    file.close()
