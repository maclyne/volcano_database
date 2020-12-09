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
    
    # Step 1: Extract out columns of interest. Such as volcano, date, latitude,
    # and SO2 expellation

    # extracts the desired columns for stratospheric volcanos
    volcano_data = my_utils.get_column(args.file_name, args.query_column,
                            args.query_value, args.result_columns)
    
    # writes CVS file from extracted data
    fout = open(args.out_file, 'w')
    # creates header
    fout.write('volcano, date, latitude, so2_output' + '\n')
    # adds data
    for volcano, date, latitude, so2_output in volcano_data:
        fout.write(volcano + ',' + date + ',' + latitude + ',' + so2_output + '\n')
        
    fout.close()
    
    

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
