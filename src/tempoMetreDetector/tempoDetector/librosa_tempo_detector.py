import logging
import numpy as np
from tempometredetector.tempodetector import common
from utilities import plots
from .base_tempo_detector import BaseTempoDetector
from .tempo_detector_data import TempoDetectorData
import librosa


class LibrosaTempoDetector(BaseTempoDetector):
    def __str__(self):
        return "LibrosaTempoDetector"

    def detect_tempo(self, detect_data: TempoDetectorData):
        audio, sampling_frequency = librosa.load(path=detect_data.path)
        onset = librosa.onset.onset_strength(audio, sr=sampling_frequency)
        librosa_tempo = librosa.beat.tempo(
            audio, sr=sampling_frequency, onset_envelope=onset
        )
        return librosa_tempo[0]
