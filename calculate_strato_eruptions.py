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
    parser.add_argument('--query_columns',
                        dest='query_columns',
                        required=True,
                        nargs='+',
                        help='Columns containing plume altitude and'
                        + 'tropopause height')
    parser.add_argument('--out_file',
                        dest='out_file',
                        type=str,
                        required=True,
                        help='File name of CSV file to be created.')
    args = parser.parse_args()
    # calculates whether volcano plume reached stratosphere
    # returns y or n in a list 
    stratospheric = my_utils.check_plume_height(args.file_name, args.query_columns)
    
    strato_column = 'Stratospheric_(y/n)'
    
    # adds stratospheric y/n list to data set
    updated_CSV_stratospheric = bin_utils.add_column_csv(args.file_name, args.out_file, strato_column, stratospheric)


if __name__ == '__main__':
    main()