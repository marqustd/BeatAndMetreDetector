import unittest
from utilities import find_last_index_of_less_or_equal


class Tests(unittest.TestCase):
    def test_find_last_index_of_less_or_equal(self):
        list = [1, 2, 1, 3, 4, 5]
        result = find_last_index_of_less_or_equal(list, 1)
        self.assertEqual(result, 2)


if __name__ == '__main__':
    unittest.main()
