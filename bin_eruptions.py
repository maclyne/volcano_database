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
    args = parser.parse_args()

    # Step 1: Extract out columns of interest. Such as date, latitude,
    # SO2 expellation, and plume height.
    # The goal is to make this part as user friendly as possible by
    # allowing string input of columns as well as integer input.
    Column_out = get_column(args.file_name, args.query_column,
                            args.query_value, args.result_columns)
    print(Column_out)

    # Step 2: Bin volcanos spatially and temporally

    # 2a (Temporal): Run function that calculates SO2 decay reactions
    # to take into account volcanos that happened near the same time
    # adding together their atmosphereic emmission. Stratopshereic
    # volcano plumes would have a larger impact on this factor

    # 2b (Spatial): Run function that collects the volcanos based on
    # how close they are latitudally, taking into account the global
    # wind patterns.

    # Step 3: Plot the data
    # Show the result of the binned data in a plot similar to shown in
    # class with axises of time and latitude.
    # Also potentially create a plot suggesting the combined impact of the
    # binned volcanoes on global temperature.


if __name__ == '__main__':
    main()
