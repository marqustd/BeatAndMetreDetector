import numpy as np


def euclidian_distance(oneBin, secondBin):
    return np.sum(np.square(oneBin - secondBin))


def cosine_distance(oneBin, secondBin):
    return 1 - np.sum(np.square(oneBin * secondBin)) / (
        np.sqrt(np.sum(np.square(oneBin))) * np.sqrt(sum(np.square(secondBin)))
    )


def kullback_leibler(oneBin, secondBin):
    return np.sum(oneBin * np.log(oneBin / secondBin))


def calculate_bsm(spectrogram, method):
    bins_amount = len(spectrogram[0])
    bsm = np.zeros((bins_amount, bins_amount))

    for x in range(bins_amount):
        this_bin = spectrogram[:, x]
        for y in range(bins_amount):
            compared_bin = spectrogram[:, y]
            bsm[x, y] = method(this_bin, compared_bin)
    return bsm
