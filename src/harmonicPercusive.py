import numpy as np


def median_filter(array, x: int, y: int, xrange: int, yrange: int):
    xstep = int((xrange-1)/2)
    ystep = int((yrange-1)/2)
    
    slice = array[x-xstep:x+xstep+1,y-ystep:y+ystep+1]
    median = np.median(slice)
    array[x,y]=median

if __name__ == '__main__':
    spcetrogram = np.array([
        [1, 101, 3],
        [4, 5, 206],
        [7, 8, 9]])
    x=y=1
    median_filter(spcetrogram,1,1,3,3)
    print(spcetrogram[x,y])