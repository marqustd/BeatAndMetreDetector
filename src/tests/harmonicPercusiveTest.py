from harmonicPercusive import median_filter
import unittest

import numpy as np


class Tests(unittest.TestCase):
    def test_median_filter(self):
        spectrogram = np.array([
            [1, 101, 3],
            [4, 5, 206],
            [7, 8, 9]])
        median_filter(spectrogram, 1,1,3,3)
        self.assertEqual(spectrogram[1,1],7)


if __name__ == '__main__':
    unittest.main()
