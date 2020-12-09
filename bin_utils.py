'''
Library of functions involved in binning data in CSV files

* get_bindex - given a value and a list of bin edges, returns \
               the index of the bin the value should go in

* add_column_csv - makes copy of the infile with a new last column added

Author: Margot Clyne
Created: Nov 8, 2020

File: bin_utils.py
'''
import sys
import numpy as np


def add_column_csv(infile, outfile, new_column_name, column_data):
    '''
    makes a copy of infile (outfile), with a new last column added

    Parameters:
    ----------
    infile: str   pathname/filename of infile CSV. \
                  Note: the first line of the infile must be the header

    outfile: str  pathname/filename of new outfile CSV \
                  Note: this will overwrite anything previously \
                  in outfile, if such a file already exists.

    new_column_name: str  name of header for the new column

    column_data: list   data to put into the new column \
                        Note: must be list matching the length of the \
                        number of infile lines (except for the header).

    Creates:
    --------
    writes the contents to outfile

    Returns:
    --------
    None
    '''

    # write data to new file that is a copy of old file with added column:
    fin = open(infile, 'r')
    out_line_list = []
    # get header line and remove /n
    in_header = fin.readline().rstrip() #NOTE: diff from BRAC_get_permit_data.py
    # parse through file lines
    for l in fin:
        out_line_list.append(l)
    fin.close()


    out_dataset_file = outfile
    fout = open(out_dataset_file, 'w')
    # write outfile header 
    fout.write(in_header +","+ new_column_name+" \n")
    # print all lines of previus file but with column_data added as new column
    for line in range(len(column_data)): #NOTE: this is diff from BRAC_get_permit_data.py
        new_out_line_list = out_line_list[line].strip()+','+str(column_data[line])+ '\n'
        fout.write(new_out_line_list)

    fout.close()


def get_bindex(value, bin_edges_list):
    """
    Get the index of the bin that the value should fit into from a list of bin edges.
    Currently uses built in numpy function np.digitize

    example: get_bindex(10, [-90, -30, 0, 30, 90]) = 3

    Parameters:
    ----------
    value: int (or float)      (dtype of contentents of bin_edges_list).
                    the value to find the matching bin of

    bin_edges_list: list of int (or of float)
                         list of bin edges.
                         NOTE: must be either monotonically increasing \
                                           or monotonically decreasing

    Returns:
    ---------
    bindex : int    the index of the matching bin
                    (value can be 1 to len(bin_edges_list) -1)
    """
    # determine whether bin_edges_list is increasing or decreasing
    if bin_edges_list[0] < bin_edges_list[1]:
        bin_order = 'increasing'
    elif bin_edges_list[0] > bin_edges_list[1]:
        bin_order = 'decreasing'
    else:
        print('ERROR: bin_edges_list is neither increasing or decreasing')
        # TODO: sys.exit with exit code
    
    # get the bindex using np.searchsorted
    if bin_order == 'increasing':
        bindex = np.digitize(value, bin_edges_list, right=False).tolist()
    else:
        bindex = np.digitize(value, bin_edges_list, right=True).tolist()

    return bindex

