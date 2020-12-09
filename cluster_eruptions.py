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


def cluster_eruptions_geotemporal(infile, outfile):
    """
    """
    # TODO
    return None # NOTE: placeholder until function is coded

if __name__ == '__main__':
    main()
