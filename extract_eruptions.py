'''
File: extract_eruptions.py
Author: Clair Huffine
Date: Dec 7 2020

This file extracts out columns of interest, such as volcano name, date,
latitude, and SO2 expellation. This data is then used to create a new
CSV file.
'''

import my_utils
import bin_utils
import argparse
import sys


def main():

    parser = argparse.ArgumentParser(
             description='Get data from a column that corresponds'
             + 'to a requested value in a different column')

    parser.add_argument('--file',
                        dest='file_name',
                        type=str,
                        required=True,
                        help='File name of CSV file to be parsed.')
    parser.add_argument('--query_column',
                        dest='query_column',
                        required=True,
                        help='Column to be searched to match query_value')
    parser.add_argument('--query',
                        dest='query_value',
                        type=str,
                        required=True,
                        help='Value to be searched for in query_column')
    parser.add_argument('--result_columns',
                        dest='result_columns',
                        nargs='+',
                        required=True,
                        help='Columns to be returned')
    parser.add_argument('--out_file',
                        dest='out_file',
                        type=str,
                        required=True,
                        help='File name of CSV file to be created.')
    args = parser.parse_args()

    # extracts the desired columns for stratospheric volcanos
    volcano_data = my_utils.get_column(args.file_name,
                                       args.query_column,
                                       args.query_value,
                                       args.result_columns)

    # writes CVS file from extracted data
    fout = open(args.out_file, 'w')
    # creates header
    fout.write('volcano, date, latitude, so2_output' + '\n')
    # adds data
    for volcano, date, latitude, so2_output in volcano_data:
        fout.write(volcano + ',' + date + ',' + latitude + ','
                   + so2_output + '\n')

    fout.close()


if __name__ == '__main__':
    main()
