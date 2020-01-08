import tempoMetreDetector as tmd
import song
import argparse
import settings

from tempo import combFilterTempoDetector, convolveTempoDetector

from metre import combfilterMetreDetector, convolveNormalizedMetreDetector, combfilterNormalizedMetreDetector, \
    convolveMetreDetector


def prepare_parser():
    tempoDetectorHelp = "tempo detector method. \n Possible detectors: \n combFilterTempoDetector, " \
                        "\n convolveTempoDetector \n (default: combFilterTempoDetector) "
    metreDetectorHelp = "metre detector method. \n Possible detectors: \n detectMetreConvolve, \n detectMetre, " \
                        "\n detectMetreConvolveNormalized, \n detectMetreNormalized \n(default: detectMetreNormalized) "

    tempoParser = argparse.ArgumentParser(add_help=False)
    tempoParser.add_argument("-t", help=tempoDetectorHelp, dest='tempoDetector', default='combFilterTempoDetector')

    metreParser = argparse.ArgumentParser(add_help=False)
    metreParser.add_argument("-m", help=metreDetectorHelp, dest='metreDetector', default='detectMetreNormalized')

    parser = argparse.ArgumentParser(parents=[tempoParser, metreParser])
    parser.add_argument("song", help="path to song")
    parser.add_argument('--plots', dest='showPlots', default=False,
                        help='show plots (default: disabled)', action='store_const', const=True)
    parser.add_argument('--settings', dest='showSettings', default=False,
                        help='show used settings at the end of program (default: disabled)', action='store_const',
                        const=True)
    parser.add_argument("-p", help='Comb fiter pulses (default: 10)', dest='pulses', default=10, type=int)
    parser.add_argument("-r", help='Resampling ratio. 0 turns off resampling. (default: 4)', dest='resampleRatio',
                        default=4, type=int)
    return parser


def show_settings(tempoDetector, metreDetector):
    print("Settings:")
    print(f"Combfilter pulses: {settings.combFilterPulses}")
    print(f"Resample ratio: {settings.resampleRatio}")
    print(f"Tempo detection method: {tempoDetector}")
    print(f"Metre detection method: {metreDetector}")


def parse_tempo_detector(detector: str):
    if detector == 'combFilterTempoDetector':
        return combFilterTempoDetector.CombFilterTempoDetector()
    elif detector == 'convolveTempoDetector':
        return convolveTempoDetector.ConvolveTempoDetector()
    else:
        return None


def parse_metre_detector(detector: str):
    if detector == 'detectMetre':
        return combfilterMetreDetector.CombfilterMetreDetector()
    elif detector == 'detectMetreNormalized':
        return combfilterNormalizedMetreDetector.CombfilterNormalizedMetreDetector()
    elif detector == 'detectMetreConvolve':
        return convolveMetreDetector.ConvolveMetreDetector()
    elif detector == 'detectMetreConvolveNormalized':
        return convolveNormalizedMetreDetector.ConvolveNormalizedMetreDetector()
    else:
        return None


def parse_resample_ratio(resampleRatio, parser):
    if resampleRatio < 0:
        parser.error("Resample ratio has to be positive or zero!")
    elif resampleRatio == 0:
        settings.resampleSignal = False
    else:
        settings.resampleRatio = resampleRatio


def parse_show_plots(showPlots):
    if not showPlots:
        settings.drawCombFilterPlots = False
        settings.drawPlots = False
        settings.drawFftPlots = False
        settings.drawSongBpmEnergyPlot = False
    else:
        settings.drawCombFilterPlots = True
        settings.drawPlots = True
        settings.drawFftPlots = True
        settings.drawSongBpmEnergyPlot = True


parser = prepare_parser()
args = parser.parse_args()
metreDetector = parse_metre_detector(args.metreDetector)
if metreDetector is None:
    parser.error("Wrong metreDetector provided")
tempoDetector = parse_tempo_detector(args.tempoDetector)
if tempoDetector is None:
    parser.error("Wrong tempoDetector provided")
parse_show_plots(args.showPlots)
parse_resample_ratio(args.resampleRatio, parser)
if args.pulses >= 0:
    settings.combFilterPulses = args.pulses
else:
    parser.error("Pulses amount has to be positive!")
detector = tmd.TempoMetreDetector(tempoDetector, metreDetector)
song = song.Song(args.song)
tempo, metre, time = detector.detect_tempo_metre(song)
print()
print("Song tempo: ", tempo)
print("Song metre: ", metre)
if args.showSettings:
    print()
    show_settings(tempoDetector, metreDetector)
