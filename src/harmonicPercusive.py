import numpy as np


def median_filter(array, xrange: int, yrange: int):
    for x in range(len(array)):
        for y in range(len(array[0])):
            median_filter_step(array, x, y, xrange, yrange)


def median_filter_step(array, x: int, y: int, xrange: int, yrange: int):
    xstep = int((xrange-1)/2)
    ystep = int((yrange-1)/2)

    xleft = x-xstep
    if xleft < 0:
        xleft = 0

    xright = x + xstep
    if xright > len(array)-1:
        xright = len(array)-1

    yleft = y-ystep
    if yleft < 0:
        yleft = 0

    yright = y + ystep
    if yright > len(array[0])-1:
        yright = len(array[0])-1

    slice = array[xleft:xright+1, yleft:yright+1]
    median = np.median(slice)
    array[x, y] = median


if __name__ == '__main__':
    spcetrogram = np.array([
        [1, 101, 3, 314],
        [4, 5, 206, 728],
        [4, 5, 206, 728],
        [7, 8, 9, 1]])
    x = y = 1
    median_filter(spcetrogram, 3, 3)
    print(spcetrogram)
