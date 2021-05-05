import unittest
from utilities import findLastIndexOfLessOrEqual


class Tests(unittest.TestCase):
    def testFindLastIndex(self):
        list = [1,2,1,3,4,5]
        result = findLastIndexOfLessOrEqual(list, 1)
        self.assertEqual(result, 2)


if __name__ == '__main__':
    unittest.main()
