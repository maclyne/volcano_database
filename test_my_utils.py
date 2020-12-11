import unittest
import my_utils
import numpy as np
from array import array


def main():
    unittest.main()


class TestGetColumn(unittest.TestCase):
    def test_stringinput(self):
        output = my_utils.get_column('data_testset.csv', 'county',
                                     'Boulder', 'cases')
        self.assertEqual(output[0:5], [1, 7, 7, 8, 8])

    def test_IntegerInput(self):
        output = my_utils.get_column('data_testset.csv', 'county', 'Boulder',
                                     4)
        self.assertEqual(output[0:5], [1, 7, 7, 8, 8])
        output = my_utils.get_column('data_testset.csv', 1, 'Boulder', 'cases')
        self.assertEqual(output[0:5], [1, 7, 7, 8, 8])
        output = my_utils.get_column('data_testset.csv', 1, 'Boulder', 4)
        self.assertEqual(output[0:5], [1, 7, 7, 8, 8])

    def test_MultipleResultColumns(self):
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

        # test county query with string and integer input
        output = my_utils.get_column('data_testset.csv', 'county',
                                     'Boulder', ['county', 2, 'fips'])
        correct = [['Boulder', 'Colorado', '08013']]*18
        self.assertListEqual(output, correct)

    def test_VolcanoDataSet(self):
        # simple one line desired
        output = my_utils.get_column('Aubry_2017_Table_S2_database_volcano_parameters.csv', 'Volcano',
                                     'Calbuco', ['Latitude', 'Longitude'])
        correct = ['-41.326', '-72.614']
        self.assertListEqual(output[0],correct)
        
        # find data past extra ',' in headerline
        output = my_utils.get_column('Aubry_2017_Table_S2_database_volcano_parameters.csv', 'Volcano',
                                     'Calbuco', 'Vent altitude (m a.s.l.)')
        correct = [2003, 2003]
        self.assertListEqual(output,correct)
        
        # multiple eruptions wanted and multiple results
        output = my_utils.get_column('Aubry_2017_Table_S2_database_volcano_parameters.csv', 'Volcano',
                                     'Calbuco', ['Date start (UTC)','Vent altitude (m a.s.l.)'])
        correct = [['4/22/2015 21:04', '2003'], ['4/23/2015 3:54', '2003']]
        self.assertListEqual(output,correct)

    def test_ErrorModes(self):
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
        output = my_utils.get_column('data_testset.csv', 2, 'Fort Collins', 'cases')
        self.assertEqual(output, [])

class TestCheckPlumeHeight(unittest.TestCase):
    def test_datatestset(self):
        output = my_utils.check_plume_height('data_testset.csv', ['cases', 'deaths'])
        self.assertEqual(output[0:3], ['y', 'y', 'y'])

    def test_volcanodataset(self):
        output = my_utils.check_plume_height('carn_MSVOLSO2L4_forclassproject.csv', ['alt', 'tropo'])
        self.assertEqual(output[0:4], ['y', 'y', 'y', 'n'])


if __name__ == '__main__':
    main()
