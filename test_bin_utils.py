"""Testing library of functions in bin_utils.py

    Initial date: 8 Nov 2020
    Author: Margot Clyne
"""
import unittest
import bin_utils
import array
import random
import numpy as np
import datetime
from datetime import date


class TestCalc(unittest.TestCase):
    def test_get_bindex_increasing(self):
        value = 10
        bin_edges_list = [-90, -60, -30, -15, 0, 15, 30, 60, 90]
        result = 5
        self.assertEqual(bin_utils.get_bindex(value, bin_edges_list), result)

    def test_get_bindex_decreasing(self):
        value = 10
        bin_edges_list = [90, 60, 30, 15, 0, -15, -30, -60, -90]
        result = 4
        self.assertEqual(bin_utils.get_bindex(value, bin_edges_list), result)

    def test_ErrorModes(self):
        # bin_edges_list neither increasing or decreasing monotonically
        value = 10
        bin_edges_list = [90, 90, 90, 15, 0, -15, -30, -60, -90]
        with self.assertRaises(SystemExit) as cm:
            bin_utils.get_bindex(value, bin_edges_list)
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
