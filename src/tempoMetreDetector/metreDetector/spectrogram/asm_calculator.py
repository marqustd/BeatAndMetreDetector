import numpy as np


def euclidian_distance(oneBin, secondBin):
    return (np.sum(np.square(oneBin - secondBin)),)


def cosine_distance(oneBin, secondBin):
    return 1 - np.sum(np.square(oneBin * secondBin)) / (
        np.sqrt(np.sum(np.square(oneBin))) * np.sqrt(sum(np.square(secondBin)))
    )


def kullback_leibler(oneBin, secondBin):
    return np.sum(oneBin * np.log(oneBin / secondBin))


def calculate_asm(spectrogram, times, method):
    binsAmount = len(times)
    asm = np.zeros((binsAmount, binsAmount))

    for x in range(binsAmount):
        thisBin = spectrogram[:, x]
        for y in range(binsAmount):
            comparedBin = spectrogram[:, y]
            asm_value = method(thisBin, comparedBin)
            asm[x, y] = asm_value
    return asm
