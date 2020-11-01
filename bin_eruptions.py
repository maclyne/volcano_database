from my_utils import get_column
from my_utils import identify_column
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
                        help='File name to be parsed.')
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
                        help='Column to be returned')
    args = parser.parse_args()
    
    Column_out = get_column(args.file_name, args.query_column,
                            args.query_value, args.result_columns)
    print(Column_out)

if __name__ == '__main__':
    main()
