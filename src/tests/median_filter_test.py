from tempometredetector.metredetector.spectrogram.median_filter import (
    median_filter,
    median_filter_step,
)
import unittest

import numpy as np


class Tests(unittest.TestCase):
    def test_median_filter_step_square(self):
        spectrogram = np.array([[1, 101, 3], [4, 5, 206], [7, 8, 9]])
        result = median_filter_step(spectrogram, 1, 1, 3, 3)
        self.assertEqual(result, 7)

    def test_median_filter_step_vertical(self):
        spectrogram = np.array([[1, 9, 3], [19, 8, 3], [7, 206, 1]])
        result = median_filter_step(spectrogram, 1, 1, 3, 0)
        self.assertEqual(result, 9)

    def test_median_filter_step_horizontal(self):
        spectrogram = np.array([[1, 101, 3], [17, 8, 206], [7, 8, 9]])
        result = median_filter_step(spectrogram, 1, 1, 0, 3)
        self.assertEqual(result, 17)

    def test_median_filter_square(self):
        spectrogram = np.array(
            [[13, 15, 17, 18], [123, 5466, 1, 51], [456, 12, 54, 54], [1, 235, 54, 34]]
        )
        result = median_filter(spectrogram, 3, 3)

        self.assertEqual(result[0, 0], 69)
        self.assertEqual(result[1, 1], 17)
        self.assertEqual(result[2, 2], 54)
        self.assertEqual(result[3, 3], 54)

    def test_median_filter_horizontal(self):
        spectrogram = np.array(
            [[13, 15, 17, 18], [123, 5466, 1, 51], [456, 12, 54, 54], [1, 235, 54, 34]]
        )
        result = median_filter(spectrogram, 0, 3)

        self.assertEqual(result[0, 0], 14)
        self.assertEqual(result[1, 1], 123)
        self.assertEqual(result[2, 2], 54)
        self.assertEqual(result[3, 3], 44)

    def test_median_filter_vertical(self):
        spectrogram = np.array(
            [[13, 15, 17, 18], [123, 5466, 1, 51], [456, 12, 54, 54], [1, 235, 54, 34]]
        )
        result = median_filter(spectrogram, 3, 0)

        self.assertEqual(result[0, 0], 68)
        self.assertEqual(result[1, 1], 15)
        self.assertEqual(result[2, 2], 54)
        self.assertEqual(result[3, 3], 44)


if __name__ == "__main__":
    unittest.main()
