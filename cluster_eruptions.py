"""
Cluster stratospheric volcanic eruption data spatially by latitude zone,
        and then temporally by injection date and volcanic cloud expected
        lifetime proximity.

File: cluster_eruptions.py

Author: Margot Clyne
Date : Nov 8 2020

* main - inputs the major arguments from get_args and determines (calls)
         which function to run.

* get_args - arg parser

* bin_by_latzone - determines the latitude zone bin of the volcanos in
          the infile, and writes a new outfile that is a copy of the
          infile but with new column named latbin_zone at the end.

* cluster_eruptions_geotemporal - # TODO

* identify_volcano_size - Identifies and bins volcanos by size from
          time_cluster_info_file. The output clusters have info of
          latbin_zone, size_unit, and coverage_time

"""
import sys
import argparse
from bin_utils import get_bindex
from bin_utils import add_column_csv
import my_utils
import datetime
from datetime import date
from datetime import timedelta
import numpy as np


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
        lat_bin_edges = args.lat_bin_edges
        cluster_eruptions_geotemporal(infile, outfile, lat_bin_edges)
    elif function_command == 'identify_volcano_size':
        identify_volcano_size(infile,
                              outfile,
                              args.SO2_output_column,
                              args.time_cluster_info_file)
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

    parser.add_argument('-lat_column',
                        type=int,
                        help='index of latitude column in infile',
                        default=1)

    parser.add_argument('-lat_bin_edges',
                        type=int,
                        nargs='+',
                        help='list of int declaring the latitude bin edges')

    parser.add_argument('-SO2_output_column',
                        help='index of SO2_output column in infile',
                        type=int,
                        default=1)

    parser.add_argument('-time_cluster_info_file',
                        type=str,
                        help='Name of the time_cluster_info CSV file')

    return parser


def bin_by_latzone(infile, outfile, lat_column, lat_bin_edges):
    """
    Determines the latitude zone bin of the volcanos in the infile, and
    writes a new outfile that is a copy of the infile but with a new column
    named latbin_zone at the end.

    Parameters:
    ----------
    infile : str   of filepath/filename that contains
                   ONLY stratospheric eruptions.
                   CSV file had columns of:
                          volcano_label,
                          latitude,
                          date,
                          mass_so2

    outfile : str  of filepath/filename that will be created.
                   This new file is a copy of infile, but with an additional
                   last column of latbin_zone, which is an integer
                   corresponding to the latitude zone bin matched in
                   get_bindex for the volcanos latitude and the lat_bin_edges.

    lat_column : int        index of the latitude column in infile

    lat_bin_edges : list of int  declaring what the latitude bin edges will be.
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


def cluster_eruptions_geotemporal(infile, outfile, lat_bin_edges):
    """
    clusters volcanic eruptions in each latzone by time proximity.
    The output clusters have info of latbin_zone, binned_date, binned_mass_so2
    This is all output to a CSV file.


    Parameters:
    ----------
    infile : str   of filepath/filename that contains
                   ONLY stratospheric eruptions.
                   CSV file has columns of:
                          volcano_label,
                          latitude,
                          date,
                          mass_so2,
                          latbin_zone,
                          size_unit,
                          coverage_time_years

    outfile : str  of filepath/filename that will be created.
                        The CSV columns will be:
                        latbin_zone, binned_date, binned_mass_so2


    lat_bin_edges : list of int  declaring what the latitude bin edges will be.
                            example: [-90, -60, -30, -15, 0, 15, 30, 60, 90]

    """

    # convert time to date format
    one_year = 365

    # pre-allocate structure of out_data list of lists of lists
    #   out_data[0] will be lat_bin_list
    #   out_data[1] will be list of binned_date for each latbin_zone
    #   out_data[2] will be list of binned_mass_so2 for each latbin_zone
    out_data = [[], [], []]
    z_used = []
    # Get volcano data
    num_latbins = len(lat_bin_edges) - 1
    lat_bin_list = range(1, num_latbins + 1)

    latbin_zone_column = 4  # NOTE: these column values are currently hardcoded
    date_column = 1
    mass_column = 3
    volc_size_column = 5
    volc_coverage_time_column = 6

    # for each latbin_zone
    for z in range(num_latbins):
        data = my_utils.get_column(infile,
                                   query_column=latbin_zone_column,
                                   query_value=str(lat_bin_list[z]),
                                   result_column=[date_column, mass_column,
                                                  volc_size_column,
                                                  volc_coverage_time_column])

        volc_date_list = [date.fromisoformat(data[i][0]) for i in range(len(data))]
        volc_mass_list = [float(data[i][1]) for i in range(len(data))]
        volc_size_list = [int(data[i][2]) for i in range(len(data))]
        volc_coverage_time_list = [float(data[i][3]) for i in range(len(data))]

        # skip the current latbin_zone if the data for it is empty
        if volc_date_list == []:
            continue

        # prep lists
        z_used.append(z)
        out_data[0].append(lat_bin_list[z])
        binned_date_list = []
        binned_mass_list = []

        # keep track of which volcanoes have been used up.
        # If it has been used, change volc_used_array[v_ind] from 0 to 1
        volc_used_array = np.zeros(len(volc_date_list))

        # start with biggest volc_size in the time_cluster_info_file
        volc_size_iterator = max(volc_size_list)

        # for this volc_size and coverage_time :
        while volc_size_iterator > 0:
            # find first instance (in time) of volc_size
            # call that index v_ind.
            # If it cant be found, then return v_ind == -1
            ind_finds = np.arange(len(volc_size_list))[(np.array(volc_size_list) == volc_size_iterator) & (volc_used_array == 0)]
            if np.size(ind_finds) == 0:
                v_ind = -1
            else:
                v_ind = ind_finds[0]

            while (v_ind != -1) and (v_ind < len(volc_date_list)):
                # starting at first unused instance of v_ind
                # at this volc_size:
                binned_date = volc_date_list[v_ind]
                binned_date_list.append(binned_date)

                swath_end = binned_date + datetime.timedelta(days=int(one_year * volc_coverage_time_list[v_ind]))

                # add this first mass to binned_mass
                binned_mass = volc_mass_list[v_ind]
                volc_used_array[v_ind] = 1

                # grab any of the 3 earlier eruptions 
                #   if theyre unused and < 14 days ago
                binned_mass, volc_used_array = collect_14day_before(v_ind,
                                                                    volc_used_array,
                                                                    volc_date_list,
                                                                    binned_date,
                                                                    binned_mass,
                                                                    volc_mass_list)
                # update to next v_ind to move forward
                v_ind += 1

                # while the next volcanoes are within the swath range:
                #    # if they have already been used, skip them.
                #    # otherwise:
                #        # if they are two or more unit sizes \
                #        #  less than the current volc_size,
                #            # then add their masses to the binned_mass.
                #            # their date will be moved into \
                #            #   the time of the binned_date
                #        # If a volcano of the same or only one unit smaller \
                #        #   volc_size is encountered,
                #            # then cut short the swath there.
                #            # save the binned_mass to list and
                #            # and start the next binned_date
                #            # with a new swath_end and a new binned_mass.
                #            # (immediately save that next binned_date to list)
                # once the while loop is done (i.e. no more unused volcanos\
                #   are found within the swath range):
                #    # save the binned_mass
                #    # find the next v_ind of the next unused \
                #    #   volcano of that volc_size
                #        # if there are no unused volcanos of that volc_size,
                #            #then iterate down to next smaller volc_size \
                #            #   and start process again
                while (v_ind < len(volc_date_list)) and (volc_date_list[v_ind] < swath_end):
                    if volc_used_array[v_ind] == 1:
                        v_ind += 1
                    else:
                        if volc_size_list[v_ind] <= volc_size_iterator - 1:
                            binned_mass += volc_mass_list[v_ind]
                            volc_used_array[v_ind] = 1
                            v_ind += 1
                        else:
                            binned_mass_list.append(binned_mass)
                            binned_date = volc_date_list[v_ind]
                            binned_date_list.append(binned_date)
                            binned_mass = volc_mass_list[v_ind]
                            swath_end = binned_date + datetime.timedelta(days=one_year * volc_coverage_time_list[v_ind])
                            volc_used_array[v_ind] = 1
                            v_ind += 1
                else:
                    binned_mass_list.append(binned_mass)
                    if v_ind == len(volc_date_list):
                        v_ind -= 1
                    volc_used_array[v_ind] = 1
                # find next unused instance (in time) of volc_size
                # and call that index v_ind.
                # If it cant be found, then return v_ind == -1
                ind_finds = np.arange(len(volc_size_list))[(np.array(volc_size_list) == volc_size_iterator) & (volc_used_array == 0)]
                if np.size(ind_finds) == 0:
                    v_ind = -1
                else:
                    v_ind = ind_finds[0]
                binned_mass, volc_used_array = collect_14day_before(v_ind,
                                                                    volc_used_array,
                                                                    volc_date_list,
                                                                    binned_date,
                                                                    binned_mass,
                                                                    volc_mass_list)
                v_ind = v_ind
            # Once no remaining unused volcanos of this volc_size are found,
            # iterate down to next smaller volc_size
            else:
                volc_size_iterator = volc_size_iterator - 1

        # sort these lists by date and append to out_data lists
        list1, list2 = zip(*sorted(zip(binned_date_list, binned_mass_list)))
        binned_date_list, binned_mass_list = (list(t) for t in zip(*sorted(zip(list1, list2))))
        out_data[1].append([binned_date_list])
        out_data[2].append([binned_mass_list])

    # write out_data to a CSV file in format:
    # 'latbin_zone', 'binned_date', 'binned_mass_so2'

    fout = open(outfile, 'w')
    fout.write("latbin_zone,binned_date,binned_mass_so2 \n")
    for z in range(0, len(out_data[0])):
        for d in range(0, len(out_data[1][z][0])):
            fout.write(str(out_data[0][z]) + ',' + str(out_data[1][z][0][d]) + ',' + str(out_data[2][z][0][d]) + '\n')
    fout.close()


def collect_14day_before(v_ind, volc_used_array, volc_date_list,
                         binned_date, binned_mass, volc_mass_list):
    '''
    Check to see if any of the 3 (smaller) volcanos beforehand \
    are unused and erupted within 2 weeks of this. \
    For any that did, add their masses to binned_mass \
    and count them as used.

    NOTE: this is inly meant to be used as a helper function within \
            cluster_eruptions_geotemporal(), not a standalone funciton.
    '''
    for i in range(1, 4):
        v_ind_previous = v_ind - i
        if (v_ind_previous >= 0) and (volc_used_array[v_ind_previous] != 1):
            if volc_date_list[v_ind_previous] > binned_date - datetime.timedelta(days=15):
                binned_mass += volc_mass_list[v_ind_previous]
                volc_used_array[v_ind_previous] = 1

    return binned_mass, volc_used_array


def identify_volcano_size(infile, outfile, SO2_output_column,
                          time_cluster_info_file):
    """
    Identifies and bins volcanos by size from time_cluster_info_file.
    The output clusters have info of latbin_zone, size_unit,
    and coverage_time
    This is all output to a CSV file.
    Parameters:
    ----------
    infile : str   of filepath/filename that contains
                   ONLY stratospheric eruptions.
                   CSV file has columns of:
                          volcano_label,
                          latitude,
                          date,
                          mass_so2,
                          latbin_zone
    outfile : str  of filepath/filename that will be created.
                        The CSV columns will be:
                          volcano_label,
                          latitude,
                          date,
                          mass_so2,
                          latbin_zone,
                          size_unit,
                          coverage_time

    SO2_output_column : str or int
                        The column containing the SO2 mass output
    time_cluster_info_file : str   of filepath/filename for a CSV file that
                                    contains the coverage_time for
                                    volcanoes by their size
                                    (currently by mass so2)
    """

    f = my_utils.open_file(infile)

    # separates header line, removes /n, and splits by comma
    header = f.readline().rstrip().split(',')

    # calls the column_index function to identify the SO2_output column
    # based on either its integer or string value

    column_index = my_utils.identify_column(SO2_output_column, header)
    i = column_index

    # create Results list to add results to
    size_unit = []
    coverage_time = []

    for line in f:
        A = line.rstrip().split(',')

        # open reference file
        ref = my_utils.open_file(time_cluster_info_file)
        # skip first header line
        next(ref)

        for line2 in ref:
            r = line2.rstrip().split(',')
            # where SO2 mass falls within preset ranges
            if int(A[i]) >= int(r[0]) and int(A[i]) <= int(r[1]):
                size_unit.append(r[2])
                coverage_time.append(r[3])
                break
            else:
                continue

    f.close()
    ref.close()

    # add columns with data to the file
    add_column_csv(infile, outfile, 'size_unit', size_unit)
    add_column_csv(outfile, outfile, 'coverage_time_years', coverage_time)


if __name__ == '__main__':
    main()
