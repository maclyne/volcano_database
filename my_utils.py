"""Collects data from a column within a dataset

    * get_column - searches through a data file and finds
                   specific values relating to an inputted search
                   parameter(s).

    * identify_column - Identifies the query and result columns of interest
                   if entered as an integer or a string and gives the index
                   values of those columns. """
from array import array
from operator import itemgetter
import matplotlib
import matplotlib.pylab as plt
import sys
from datetime import datetime
matplotlib.use('Agg')


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
    column_index = identify_column(query_column, result_column, header)
    # query column index
    i = column_index[0]
    # result column index
    ii = column_index[1]

    # sets Result output type based on number of inputted result columns
    if type(result_column) is list:
        # create Results list to add results to with multiple result columns
        Output = []
    else:
        # creates Result array to add results to with one result column
        Output = array('i', [])

    for line in f:
        A = line.rstrip().split(',')
        # checks if value in the query_column matches the inputted query_value
        if A[i] == query_value:

            try:
                # keeps track of date
                curr_date = datetime.strptime(A[0], '%Y-%m-%d')
                if last_date is not None:
                    delta = curr_date - last_date
                    # checks for skipped days and pads
                    if delta.days > 1:
                        for j in range(delta.days - 1):
                            Output.append(Output[-1])
                    # checks for out of order days
                    elif delta.days < 0:
                        raise ValueError
                last_date = curr_date

            # handles a lack of date column in data set
            except ValueError:
                try:
                    delta.days < 0
                    raise ValueError
                except UnboundLocalError:
                    last_date = None

            # appends value in the result columns to the outputted Result list
            if type(result_column) is list:
                case = []
                for column in result_column:
                    case.append(A[int(column)])
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


def identify_column(query_column, result_column, header):

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

    # generates variable i to indicate the query column
    i = 0
    for column_header in header:
        # checks if integer for column was inputted
        # assumes counting starting at 1
        try:
            type(int(query_column)) == int
            query_column = int(query_column)
            # checks for array length exception
            if query_column > len(header):
                print("Searching for query column "
                      + str(query_column)
                      + " but there are only "
                      + str(len(header)-1)
                      + " fields")
                sys.exit(1)
            else:
                i = query_column - 1
        except ValueError:
            if query_column == column_header:
                break
            else:
                i += 1
                # checks for str(query_column) match exception
                if i > (len(header) - 1):
                    print("Searching for query column "
                          + query_column
                          + " but this file does not contain it")
                    sys.exit(1)

    # generates variable ii to indicate the result column
    ii = 0
    if type(result_column) is not list:
        # checks if integer for column was inputted
        # assumes counting starting at 1
        for column_header2 in header:
            try:
                type(int(result_column)) == int
                result_column = int(result_column)
                # checks for array length exception
                if result_column > (len(header) - 1):
                    print("Searching for result column "
                          + str(result_column)
                          + " but there are only "
                          + str(len(header)-1)
                          + " fields")
                    sys.exit(1)
                else:
                    ii = result_column - 1
            except ValueError:
                if result_column == column_header2:
                    break
                else:
                    ii += 1
                    # checks for str(query_column) match exception
                    if ii > (len(header)-1):
                        print("Searching for result column "
                              + result_column
                              + " but this file does not contain it")
                        sys.exit(1)
    else:
        for column in result_column:
            # checks for array length exception
            if int(column) > (len(header)-1):
                print("Searching for result column "
                      + str(column)
                      + " but there are only "
                      + str(len(header)-1)
                      + " fields")
                sys.exit(1)
    return(i, ii)
