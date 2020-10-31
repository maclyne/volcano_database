import unittest
import my_utils
import numpy as np
from array import array

# TODO: updated with relevant example dataset

def main():
    unittest.main()

class TestGetColumn(unittest.TestCase):
    def test_stringinput(self):
        output = my_utils.get_column('data_testset.csv', 'county',
                                     'Boulder', 'cases')
        self.assertEqual(output[0:5], [1, 7, 7, 8, 8])

    def testIntegerInput(self):
        output = my_utils.get_column('data_testset.csv', 'county', 'Boulder', 4)
        self.assertEqual(output[0:5], [1, 7, 7, 8, 8])
        output = my_utils.get_column('data_testset.csv', 1, 'Boulder', 'cases')
        self.assertEqual(output[0:5], [1, 7, 7, 8, 8])
        output = my_utils.get_column('data_testset.csv', 1, 'Boulder', 4)
        self.assertEqual(output[0:5], [1, 7, 7, 8, 8])

    def testMultipleResultColumns(self):
        # test county query with integer input
        output = my_utils.get_column('data_testset.csv', 'county',
                                     'Boulder', [1, 2, 3])
        correct = [['Boulder', 'Colorado', '08013']]*18
        self.assertListEqual(output, correct)
               
        # test county query with string input
        output = my_utils.get_column('data_testset.csv', 'county',
                                     'Boulder', ['county', 'state', 'fips'])
        correct = [['Boulder', 'Colorado', '08013']]*18
        self.assertListEqual(output, correct)

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
