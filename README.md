# Volcanic Eruption Data Binning

## Authors: Margot Clyne and Clair Huffine
## Created: October 28 2020
## Last Updated: December 10 2020

## This project applies software engineering best practices to the spatial and temporal binning of volcanic eruptions over the past century to better include their impact on global temperature abnormalities. 

This project works with data from [TODO: ADD PAPER WHERE DATA IS SOURCED FROM]. The workflow of this project in Snakefile is pictured below:

<center><img src="[add dag.png here]" width="300"/></center>

1. The script **calculate_strato_eruptions.py** allows for input to select the CSV file name, the query columns, and the output file name. For this project, it determines if the volcanoic erpuptions reached the stratosphere based on the eruption altitude (alt) and the height in km of the troposhere at the location of the volcano (tropo) and adds 'y' or 'n' to the data within the original CSV file as a new column and creates and outputs a new CSV file (Updated_data.csv).

2. The script **extract_eruptions.py** allows for input to select the CSV file name, query column, query value, and result columns. Functions in my_utils.py are used to search through the file (Updated_data.csv) for a specified volcano, date, latitude, and SO2 expellation and collects the requested data from the reult columns of interest. This data is then used to create a new CSV file (Data1.csv).

3. The function **bin_by_latzone** in the script **cluster_eruptions.py** allows for input to select the CSV file, the output file name, the latitude column, and the latitude bin edges. This function is used to determine the latitude zone bin of the volcanos in the infile (Data1.csv), and writes a new outfile (Data2.csv) that is a copy of the infile but with new column named latbin_zone at the end.

4. The function **identify_volcano_size** in the script **cluster_eruptions.py** allows for input to select the CSV file, the output file name, the SO2 output column, and the CSV file containing the time cluster information. This function  used the data in Data2.csv and identifies and bins volcanos by size based on the ranges and coverage time set in time_cluster_info_file.csv. The output (Data3.csv) is a copy of the infile but with new columns named size_unit and coverage_time at the end. 

5. The function **cluster_eruptions_geotemporal** in the script **cluster_eruptions.py** allows for input to select the CSV file, the output file name, [TODO: UPDATE once completed]

6. The script **plot_volcano_clustered_timeseries_plot.png** creates four subplots:

    subplot(0,0) and subplot (0,1) will be the same. (Plot A)
    subplot(1,0) and subplot (1,1) will be (Plot C) and (Plot D)

    Plot A: Classic Timeseries Line plot where:
        x-axis = Date
        y-axis = Global Temperature data (or anomoly, TBD)

    Plot C: A stem plot of the data from Data2.csv
        x-axis = Date (matching axis alighnent with subplot(0,0)
        y-axis = inverted stem plot of mass_so2 from each volcano
        colorscheme: latzones

    Plot D: A stem plot of the data from Data3.csv
        x-axis = Date (matching axis alighnent with subplot(0,1)
        y-axis = Inverted stem plot of clustered eruptions
        colorscheme: latzones (same legend as Plot B)


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
