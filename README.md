# Volcanic Eruption Data Binning

## Authors: Margot Clyne and Clair Huffine
## Created: October 28 2020
## Last Updated: December 10 2020

## This project applies software engineering best practices to the spatial and temporal binning of volcanic eruptions over the past century to better include their impact on global temperature abnormalities. 

This project works with data from [ADD PAPER WHERE DATA IS SOURCED FROM]. The workflow of this project in Snakefile is pictured below:

<center><img src="[add dag.png here]" width="300"/></center>

First, the script calculate_strado_eruptions.py determines if the volcanoic erpuptions reached the stratosphere based on the eruption altitude (alt) and the height in km of the troposhere at the location of the volcano (tropo) and add 'y' or 'n' to the data within the original CSV file as a new column and create and outputs a new CSV file (Updated_data.csv).

The script bin_eruptions.py allows for input to select the CSV file name, query column, query value, and result columns. Functions in my_utils.py are used to search through the file for a specified volcano, date, or latitude (as desired), collects the requested data from the reult columns of interest, and combines volanic output based on location and date. 

Further code will allow for plotting if this data is for visualizaiton.

***Methods Included:***
   open_file 'Opens a comma separated CSV file.'
   
   get_column 'Returns an array of integers from the result_column where the query_value matches the value in the query_column.'
   
   identify_column 'Identifies the query and result columns of interest if entered as an integer or a string and gives the index values of those columns.'

                   
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
(will add output when complete)
```
