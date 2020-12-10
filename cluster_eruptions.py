"""
Cluster stratospheric volcanic eruption data spatially by latitude zone, and then temporally by \
        injection date and volcanic cloud expected lifetime proximity.

File: cluster_eruptions.py

Author: Margot Clyne
Date : Nov 8 2020

* main - inputs the major arguments from get_args and determines (calls) which function to run

* get_args - arg parser

* bin_by_latzone - determines the latitude zone bin of the volcanos in the infile, and writes a \
            new outfile that is a copy of the infile but with \
            a new column named latbin_zone at the end.

* cluster_eruptions_geotemporal - # TODO

"""
import sys
import argparse
from bin_utils import get_bindex
from bin_utils import add_column_csv
import my_utils
from datetime import date
from datetime import timedelta

def main():
    '''
    inputs the major arguments and determines (calls) which function to run

    Required Parameters:
    ----------
    function_name : str    Name of the function in this file to run

    infile : str       Name of the input data CSV file

    outfile : str     Name of the data CSV file to be created
    
    Function Specific Parameters:
    ----------
    see get_args and doc strings of the specific function names
    '''
    # parse command line arguments
    parser = get_args('process args for main()')

    args = parser.parse_args()
    function_command = args.function_name
    infile = args.infile
    outfile = args.outfile

    # run function
    if function_command == 'bin_by_latzone':
        lat_column = args.lat_column
        lat_bin_edges = args.lat_bin_edges
        bin_by_latzone(infile, outfile, lat_column, lat_bin_edges)
    elif function_command == 'cluster_eruptions_geotemporal':
        # TODO: add to argparser for this function
        cluster_eruptions_geotemporal(infile, outfile) # TODO: add arguments

    else:
        print('function not run. check function name spelling')


def get_args(description):
    '''
    arg parser for the main function with args for sub functions as needed
    '''
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('--function_name',
                        type=str,
                        help='Name of the function in this file to run',
                        required=True)

    parser.add_argument('--infile',
                        type=str,
                        help='Name of the input data CSV file',
                        required=True)

    parser.add_argument('--outfile',
                        type=str,
                        help='Name of the data file to be created',
                        required=True)

    parser.add_argument('--lat_column',
                        type=int,
                        help='index of latitude column in infile',
                        default=1)

    parser.add_argument('--lat_bin_edges',
                        type=int,
                        nargs='+',
                        help='list of int declaring the latitude bin edges')

    return parser



def bin_by_latzone(infile, outfile, lat_column, lat_bin_edges):
    """
    determines the latitude zone bin of the volcanos in the infile, and writes a \
            new outfile that is a copy of the infile but with \
            a new column named latbin_zone at the end. 

    Parameters:
    ----------
    infile : str   of filepath/filename that contains \
                   ONLY stratospheric eruptions.
                   CSV file had columns of: \
                          volcano_label, \
                          latitude, \
                          date, \
                          mass_so2

    outfile : str  of filepath/filename that will be created.
                   This new file is a copy of infile, but with an additional \
                   last column of latbin_zone, which is an integer corresponding to \
                   the latitude zone bin matched in get_bindex for the volcanos latitude \
                   and the lat_bin_edges.

    lat_column : int        index of the latitude column in infile

    lat_bin_edges : list of int     declaring what the latitude bin edges will be. 
                                    example: [-90, -60, -30, -15, 0, 15, 30, 60, 90]

    """
    # read the infile and figure out the latbin_zones
    bindex_list = []
    f = open(infile, 'r')
    # skip first header line
    next(f)
    for line in f:
        A = line.rstrip().split(',')
        bindex_list.append(get_bindex(value=float(A[lat_column]),
                                      bin_edges_list=lat_bin_edges))

    f.close()
    new_column_name = 'latbin_zone'
    # write copy of infile to outfile with latbin_zone column added
    add_column_csv(infile, outfile, new_column_name, column_data=bindex_list)


def cluster_eruptions_geotemporal(infile, outfile, time_cluster_info_file,
                                  lat_bin_edges):
    """
    clusters volcanic eruptions in each latzone by time proximity.
    The output clusters have info of latbin_zone, binned_date, binned_mass_so2
    This is all output to a CSV file.


    Parameters:
    ----------
    infile : str   of filepath/filename that contains \
                   ONLY stratospheric eruptions.
                   CSV file has columns of: \
                          volcano_label, \
                          latitude, \
                          date, \
                          mass_so2, \
                          latbin_zone

    outfile : str  of filepath/filename that will be created.
                        The CSV columns will be:
                        latbin_zone, binned_date, binned_mass_so2

    time_cluster_info_file : str   of filepath/filename for a CSV file that \
                                    contains the coverage_time for \
                                    volcanoes by their size (currently by mass so2)

    lat_bin_edges : list of int     declaring what the latitude bin edges will be. 
                                    example: [-90, -60, -30, -15, 0, 15, 30, 60, 90]
    """
    #TODO: get time_cluster_info_file data
    


    # TODO: assign size to each volcano


    # Get volcano data
    latbin_zone_column = 4
    num_latbins = len(lat_bin_edges) -1
    lat_bin_list = range(1, num_latbins +1)

    latbin_zone_column = 4
    date_column = 2
    mass_column = 3

    # for each latbin_zone
    for z in range(num_latbins):
        data = get_column(infile,
                          query_column=latbin_zone_column,
                          query_value=lat_bin_list[z],
                          result_columns=[date_column, mass_column])
        volc_date_list = [date.fromisoformat(i) for i in data[0]]
        volc_mass_list = [float(i) for i in data[1]]
        # NOTE: idk if Clairs version of get_column has the same input and output args order as mine
    

        # TODO: start with biggest volc_size in the time_cluster_info_file
        volc_size = max(volc_size_keys) #NOTE: I made up these names. 
        coverage_time = coverage_time_values(volc_size) #NOTE: I made up these names. 
        # do something

        # find first instance (in time) of volc_size

        # TODO: iterate down to next smaller volc_size
        volc_size = volc_size - 1


def identify_volcano_size(infile, outfile, SO2_output_column, time_cluster_info_file):
    """
    Identifies and bins volcanos by size from time_cluster_info_file.
    The output clusters have info of latbin_zone, binned_mass_so2,
    and coverage_time
    This is all output to a CSV file.


    Parameters:
    ----------
    infile : str   of filepath/filename that contains \
                   ONLY stratospheric eruptions.
                   CSV file has columns of: \
                          volcano_label, \
                          latitude, \
                          date, \
                          mass_so2, \
                          latbin_zone

    outfile : str  of filepath/filename that will be created.
                        The CSV columns will be:
                        latbin_zone, binned_mass_so2, and coverage_time
    
    SO2_output_column : str or int
                        The column containing the SO2 mass output

    time_cluster_info_file : str   of filepath/filename for a CSV file that \
                                    contains the coverage_time for \
                                    volcanoes by their size (currently by mass so2)
    """
    
    f = my_utils.open_file(infile)
    ref = my_utils.open_file(time_cluster_info_file)
    
    # skip first header line
    next(ref)
    
    # separates header line and removes /n
    header_unsplit = f.readline().rstrip()
    # splits header. The gibberish is to not split based on commas in ()
    header = re.split(r',(?!(?:[^(]*\([^)]*\))*[^()]*\))', header_unsplit)

    # calls the column_index function to identify the SO2_output column
    # based on either its integer or string value
    i = []

    column_index = identify_column(SO2_output_column, header)
    i.append(column_index)

    # create Results list to add results to
    size_unit = []
    coverage_time = []

    for line in f:
        A = line.rstrip().split(',')
        for line2 in ref:
            r = line2.rstrip().split(',')
            # where SO2 mass falls within preset ranges
            if A[i] >= r[0] and A[i] <= r[1]:
                size_unit.append(r[2])
                coverage_time.append(r[3])
            else:
                continue
    f.close()
    ref.close()
    
    # add columns with data to the file
    add_column_csv(infile, out_file, 'size_unit', size_unit)
    add_column_csv(out_file, out_file, 'coverage_time_years', coverage_time)


if __name__ == '__main__':
    main()
