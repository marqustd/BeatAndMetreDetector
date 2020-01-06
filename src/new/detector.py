import tempoMetreDetector as tmd
import song
import argparse
import settings

import combFilterTempoDetector
import convolveTempoDetector

import detectMetreConvolve
import detectMetre
import detectMetreConvolveNormalized
import detectMetreNormalized


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
    parser.add_argument("song", help="Path to song")
    parser.add_argument('--plots', dest='showPlots', default=False,
                        help='show plots (default: disabled)', action='store_const', const=True)
    return parser


def parse_tempo_detector(detector: str):
    if detector == 'combFilterTempoDetector':
        return combFilterTempoDetector.CombFilterTempoDetector()
    elif detector == 'convolveTempoDetector':
        return convolveTempoDetector.ConvolveTempoDetector()
    else:
        return None

def parse_metre_detector(detector: str):
    if detector == 'detectMetre':
        return detectMetre.DetectMetre()
    elif detector == 'detectMetreNormalized':
        return detectMetreNormalized.DetectMetreNormalized()
    elif detector == 'detectMetreConvolve':
        return detectMetreConvolve.DetectMetreConvolve()
    elif detector == 'detectMetreConvolveNormalized':
        return detectMetreConvolveNormalized.DetectMetreConvolveNormalized()
    else:
        return None

def parse_show_plots(showPlots):
    if not showPlots:
        settings.drawCombFilterPlots = False
        settings.drawPlots = False
        settings.drawFftPlots = False
        settings.drawSongBpmEnergyPlot = False


parser = prepare_parser()
args = parser.parse_args()
metreDetector = parse_metre_detector(args.metreDetector)
if metreDetector is None:
    parser.error("Wrong metreDetector provided")
tempoDetector = parse_tempo_detector(args.tempoDetector)
if tempoDetector is None:
    parser.error("Wrong tempoDetector provided")
parse_show_plots(args.showPlots)

detector = tmd.TempoMetreDetector(tempoDetector,metreDetector)
song = song.Song(args.song)
tempo, metre = detector.detect_tempo_metre(song)
print("Song tempo: ", tempo)
print("Song metre: ", metre)
