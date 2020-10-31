import unittest
import my_utils
import random
import numpy as np
import math
from array import array


def main():
    unittest.main()

class TestGetColumn(unittest.TestCase):
    def test_stringinput(self):
        output = my_utils.get_column('data_testset.csv', 'county',
                                     'Boulder', 'cases')
        self.assertEqual(output[0:5], array('i', [1, 7, 7, 8, 8]))

    def testIntegerInput(self):
        output = my_utils.get_column('data_testset.csv', 2, 'Boulder', 5)
        self.assertEqual(output[0:5], array('i', [1, 7, 7, 8, 8]))

    def testPaddingSkippedDays(self):
        output = my_utils.get_column('data_testset_skippeddays.csv', 2,
                                     'Boulder', 5)
        self.assertEqual(len(output),
                         len(my_utils.get_column('data_testset.csv', 2,
                                                 'Boulder', 5)))
        self.assertEqual(output[0:15],
                         array('i', [1, 7, 7, 8, 8, 11, 24, 30,
                                     30, 30, 30, 30, 30, 76, 84]))

    def testOutOfOrder(self):
        with self.assertRaises(ValueError):
            my_utils.get_column('data_testset_outoforder.csv', 2, 'Boulder', 5)

    def testErrorModes(self):
        # file not found
        with self.assertRaises(SystemExit) as cm:
            my_utils.get_column('data_testset.cs', 2, 'Boulder', 5)
        self.assertEqual(cm.exception.code, 3)

        # query column not in data set
        with self.assertRaises(SystemExit) as cm:
            my_utils.get_column('data_testset.csv', 'houses', 'Boulder', 5)
        self.assertEqual(cm.exception.code, 1)

        # query column out of bounds
        with self.assertRaises(SystemExit) as cm:
            my_utils.get_column('data_testset.csv', 80, 'Boulder', 5)
        self.assertEqual(cm.exception.code, 1)

        # result column not in data set
        with self.assertRaises(SystemExit) as cm:
            my_utils.get_column('data_testset.csv', 2, 'Boulder', 30)
        self.assertEqual(cm.exception.code, 1)

        # result column out of bounds
        with self.assertRaises(SystemExit) as cm:
            my_utils.get_column('data_testset.csv', 2, 'Boulder', 'parties')
        self.assertEqual(cm.exception.code, 1)

        # query value not in data set
        with self.assertRaises(SystemExit) as cm:
            my_utils.get_column('data_testset.csv', 2, 'Fort Collins', 'cases')
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    main()
