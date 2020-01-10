import settings


def prepare_settings_string(tempoDetector, metreDetector):
    string = "Settings:\n" \
             f"Combfilter pulses: {settings.combFilterPulses}\n" \
             f"Resample ratio: {settings.resampleRatio}\n" \
             f"Tempo detection method: {tempoDetector}\n" \
             f"Metre detection method: {metreDetector}\n"
    return string


def prepare_settings_string_filename(tempoDetector, metreDetector):
    string = f"c {settings.combFilterPulses} " \
             f"r {settings.resampleRatio} " \
             f"t {tempoDetector} " \
             f"m {metreDetector}"
    return string
