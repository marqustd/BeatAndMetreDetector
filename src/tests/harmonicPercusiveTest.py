from harmonicPercusive import median_filter
import unittest

import numpy as np


class Tests(unittest.TestCase):
    def test_median_filter_square(self):
        spectrogram = np.array([
            [1, 101, 3],
            [4, 5, 206],
            [7, 8, 9]])
        median_filter(spectrogram, 1,1,3,3)
        self.assertEqual(spectrogram[1,1],7)
        
    def test_median_filter_vertical(self):
        spectrogram = np.array([
        [1, 9, 3],
        [19, 8, 3],
        [7, 206, 1]])
        median_filter(spectrogram, 1,1,3,0)
        self.assertEqual(spectrogram[1,1],9)

    def test_median_filter_horizontal(self):
        spectrogram = np.array([
        [1, 101, 3],
        [17, 8, 206],
        [7, 8, 9]])
        median_filter(spectrogram, 1,1,0,3)
        self.assertEqual(spectrogram[1,1],17)


if __name__ == '__main__':
    unittest.main()
