# Volcanic Eruption Data Binning

## Authors: Margot Clyne and Clair Huffine
## Created: October 28 2020
## Last Updated: November 4 2020

## This project applies software engineering best practicies to the spatial and temporal binning of volcanic eruptions over the past century to better include their impact on global temperature abnormalities. 

The script bin_eruptions.py allows for input to select the CSV file name, query column, query value, and result columns. Functions in my_utils.py are used to search through the file for a specified volcano, date, or latititude (as desired), collects the requested data from the reult columns of interest, and combines volanic output based on location and date. 

***Methods Included:***
   open_file 'Opens a comma separated CSV file.'
   
   get_column 'Returns an array of intergers from the result_column where the query_value matches the value in the query_column.'
   
   identify_column 'Identifies the query and result columns of interest if entered as an integer or a string and gives the index values of those columns.'

   fill_in_column 'Opens a comma separated CSV file and fills in holes
                   in a specifiedcolumn with the string preceeding the gap.'
                   
                   
***This progam can be used through inputting the arguments outlined in print_cases.py including:*** 

***--file*** 'File name of CSV file to be parsed.'

***--query_column*** 'Column to be searched to match query_value'

***--query*** 'Value to be searched for in query_column'

***--result_columns*** 'Columns to be returned'


Tests can be viewed through the execution of the shells
```
$bash test_bin_eruptions.sh
```
Example Code:

Input
```
(will add code when complete)
```

Output:
```
(will add output when complete)\
```