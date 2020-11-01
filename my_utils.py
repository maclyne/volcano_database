"""Collects data from a column within a dataset

    * get_column - searches through a data file and finds specific values
                   relating to an inputted search parameter(s).

    * identify_column - Identifies the query columns of interest if entered
                   as an integer or a string and gives the index values of
                   those columns. """

import sys
import csv
import re

def open_file(file_name):
    """ Opens a comma separated CSV file

    Parameters
    ----------
    file_name: string
            The path to the CSV file.
    Returns:
    --------
    Output: the opened file
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
    
    # opens the file
    f = open(file_name, 'r', encoding="ISO-8859-1")
    
    return(f)

def get_column(file_name, query_column, query_value, result_column=1):

    """ Opens a comma separated CSV file and returns a list of intergers
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
    result_column: integer or string or list
            The column(s) to be returned when the row contains the query_value.
            If string, must match the data set header for that column. If an
            integer, the count must start at 0.

    Returns:
    --------
    Output: list of intergers or list of lists with multiple result column
            inputs values in the result_column matching the query_value entry.
    """
    
    f = open_file(file_name)
    
    # separates header line and removes /n
    header_unsplit = f.readline().rstrip()
    # splits header. The gibberish is to not split based on commas in ()
    header = re.split(r',(?!(?:[^(]*\([^)]*\))*[^()]*\))', header_unsplit
    
    # calls the column_index function to identify the query and result columns
    # based on either their integer or string value

    i = identify_column(query_column, header)

    ii = []
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
                try:
                    Output.append(int(A[ii]))
                except ValueError:
                    Output.append(A[ii])

    # exception for query_value not found
    if len(Output) == 0:
        print(query_value + ' was not located in the column '
              + str(query_column))
        sys.exit(1)

    return(Output)
    f.close()


def identify_column(query_column, header):

    """ Identifies the query column of interest if entered as an integer
        or a string and gives the index values of that column.

    Parameters
    ----------
    query_column: integer or string
            The column to search for the query_value in.
    header: list of strings
            The header of the file of interest which contains the column
            titles to be searched for a match with inputted strings for query
            or result columns.

    Returns:
    --------
    index: integer
            Index value of the query column.
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

def fill_in_column(file_name, column):
    """ Opens a comma separated CSV file and fills in holes in a specified
        column with the string preceeding the gap. 

    Parameters
    ----------
    file_name: string
            The path to the CSV file.
    column: integer or string
            The column to be filled in

    Returns:
    --------
    Output: updated CSV file with filled in gaps 
    """

    new_rows = [] # a holder for our modified rows when we make them
    changes = {   # a dictionary of changes to make, find 'key' substitue with 'value'
        '1 dozen' : '12', # I assume both 'key' and 'value' are strings
        }

    with open(file_name, 'rb') as f:
        # separates header line and removes /n
        header_unsplit = f.readline().rstrip()
        # splits header. The gibberish is to not split based on commas in ()
        header = re.split(r',(?!(?:[^(]*\([^)]*\))*[^()]*\))', header_unsplit

        # calls the column_index function to identify the column index
        # based on either the integer or string value
        i = identify_column(query_column, header)
        
        reader = csv.reader(f) # pass the file to our csv reader
        for row in reader:     # iterate over the rows in the file
            new_row = row      # at first, just copy the row
            for key, value in changes.items(): # iterate over 'changes' dictionary
                new_row = [ x.replace(key, value) for x in new_row ] # make the substitutions
            new_rows.append(new_row) # add the modified rows

    with open('test.csv', 'wb') as f:
        # Overwrite the old file with the modified rows
        writer = csv.writer(f)
        writer.writerows(new_rows)

    for line in f:
        A = line.rstrip().split(',')
        # checks if value in the column is empty
        if A[i] == None:
            A[i] = A[i-1]