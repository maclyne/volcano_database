"""Collects data from a column within a dataset

    * get_column - searches through a data file and finds specific values
                   relating to an inputted search parameter(s).

    * identify_column - Identifies the query and result columns of interest
                   if entered as an integer or a string and gives the index
                   values of those columns. """

from array import array
import sys
from datetime import datetime

#TODO: change output to list (not array) for single result column input

def get_column(file_name, query_column, query_value, result_column=1):

    """ Opens a comma separated CSV file and returns an array of intergers
        from the result_column where the query_value matches the value in
        the query_column.

    Parameters
    ----------
    file_name: string
            The path to the CSV file.
    query_column: integer or string
            The column to search for the query_value in.
    query_value: string
            The value to be searched for
    result_column: integer or string or tuple
            The column to be returned when the row contains the query_value.
            If a single column, works only on a string that can be made into
            an integer. If multiple columns, will work with ints only.

    Returns:
    --------
    Output: array of intergers or list of lists with multiple result column
            inputs values in the result_column matching the query_value entry.
    """

    # Checks for file not found and perrmission errors
    try:
        f = open(file_name, 'r')
    except FileNotFoundError:
        print("Couldn't find file " + file_name)
        sys.exit(3)
    except PermissionError:
        print("Couldn't access file " + file_name)
        sys.exit(4)

    f = open(file_name, 'r', encoding="ISO-8859-1")
    last_date = None

    # separates header line, removes /n, and splits into its elements
    header = f.readline().rstrip().split(',')
    
    # calls the column_index function to identify the query and result columns
    # based on either their integer or string value

    i = identify_column(query_column, header)
        
    ii=[]
    if type(result_column) is list:
        for r_column in result_column:
            column_index = identify_column(r_column, header)
            ii.append(column_index)
    else:
        ii = identify_column(result_column, header)

    # create Results list to add results to with multiple result columns
    Output = []

    for line in f:
        A = line.rstrip().split(',')
        # checks if value in the query_column matches the inputted query_value
        if A[i] == query_value:

            # appends value in the result columns to the outputted Result list
            if type(result_column) is list:
                case = []
                for index in ii:
                    case.append(A[index])
                Output.append(case)
            # appends value in the result column to the outputted Result array
            else:
                Output.append(int(A[ii]))

    # exception for query_value not found
    if len(Output) == 0:
        print(query_value + ' was not located in the column '
              + str(query_column))
        sys.exit(1)

    return(Output)
    f.close()

# TODO: update to allow multiple result columns input as strings 
    
def identify_column(query_column, header):

    """ Identifies the query and result columns of interest if entered as
        an integer or a string and gives the index values of those columns.

    Parameters
    ----------
    query_column: integer or string
            The column to search for the query_value in.
    result_column: integer or string or tuple
            The column to be returned when the row contains the query_value.
            If a single column, works only on a string that can be made into
            an integer. If multiple columns, will work with ints only.
    header: list of strings
            The header of the file of interest which contains the column
            titles to be searched for a match with inputted strings for query
            or result columns.

    Returns:
    --------
    i: integer
            Index value of the query column.
    ii: integer
            Index value of the result column.
    """
    
    index = 0
    # checks if integer for column was inputted
    # assumes counting starting at 0
    for column_header in header:
        try:
            type(int(query_column)) == int
            column = int(query_column)
            # checks for array length exception
            if column > (len(header) - 1):
                print("Searching for result column "
                      + str(query_column)
                      + " but there are only "
                      + str(len(header)-1)
                      + " fields")
                sys.exit(1)
            else:
                index = column
        except ValueError:
            if query_column == column_header:
                break
            else:
                index += 1
                # checks for str(query_column) match exception
                if index > (len(header)-1):
                    print("Searching for result column "
                          + query_column
                          + " but this file does not contain it")
                    sys.exit(1)
    return(index)
