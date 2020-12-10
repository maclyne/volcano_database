# Volcanic Eruption Data Binning

## Authors: Margot Clyne and Clair Huffine
## Created: October 28 2020
## Last Updated: December 10 2020

## This project applies software engineering best practices to the spatial and temporal binning of volcanic eruptions over the past century to better include their impact on global temperature abnormalities. 

This project works with data from [TODO: ADD PAPER WHERE DATA IS SOURCED FROM]. The workflow of this project in Snakefile is pictured below:

<center><img src="[add dag.png here]" width="300"/></center>

1. The script **calculate_strato_eruptions.py** determined if the volcanoic erpuptions reached the stratosphere based on the eruption altitude (alt) and the height in km of the troposhere at the location of the volcano (tropo) and added 'y' or 'n' to the data within the original CSV file as a new column and created and outputted a new CSV file (Updated_data.csv).

    - Inputs:
        - ***--file*** 'File name of CSV file to be parsed.'
        - ***--query_columns*** 'Columns (name or column index) containing plume altitude and tropopause height. NOTE: the value in the first input column is determined to be greater or equal to the value in the second input column.Expecting only two query columns.'
        - ***--out_file*** 'File name of CSV file to be created.'
    - Functions used:
        - my_utils.check_plume_height
        - bin_utils.add_column_csv

2. The script **extract_eruptions.py** searched through the file (Updated_data.csv) for all volcanos that reached the stratosphere and therefore contained a 'y' in the column 'Stratosphere_(y/n)' and returned the volcano, date, latitude, and SO2 expellation columns. This data was then used to create a new CSV file (Data1.csv).

    - Inputs:
        - ***--file*** 'File name of CSV file to be parsed.'
        - ***--query_column*** 'Column (name or column index) to be searched to match query_value'
        - ***--query*** 'Value to be searched for in query_column'
        - ***--result_columns*** 'Columns to be returned'
        - ***--out_file*** 'File name of CSV file to be created.'
    - Functions used:
        - my_utils.get_column

3. The function **bin_by_latzone** in the script **cluster_eruptions.py** determined the latitude zone bin of the volcanos in the infile (Data1.csv), and wrote a new outfile (Data2.csv) that was a copy of the infile but with new column named latbin_zone at the end.

    - Inputs:
        - ***--infile*** 'Name of the input data CSV file'
        - ***--outfile*** 'File name of CSV file to be created.'
        - ***-lat_column*** 'Index of latitude column in infile'
        - ***-lat_bin_edges*** 'list of int declaring the latitude bin edges. example: [-90, -60, -30, -15, 0, 15, 30, 60, 90]'
    - Functions used:
        - bin_utils.get_binindex
        - bin_utils.add_column_csv

4. The function **identify_volcano_size** in the script **cluster_eruptions.py** used the data in Data2.csv and identified and bins volcanos by size based on the ranges and coverage time set in time_cluster_info_file.csv. The output (Data3.csv) was a copy of the infile but with new columns named size_unit and coverage_time at the end. 

    - Inputs:
        - ***--infile*** 'Name of the input data CSV file'
        - ***--outfile*** 'File name of CSV file to be created.'
        - ***-SO2_output_column*** 'Index of SO2_output column in infile'
        - ***-time_cluster_info_file*** 'Name of the time_cluster_info CSV file'
    - Functions used:
        - cluster_eruptions.identify_volcano_size
        - my_utils.open_file
        - my_utils.identify_column
        - bin_utils.add_column_csv

5. The function **cluster_eruptions_geotemporal** in the script **cluster_eruptions.py** allows for input to select the CSV file, the output file name, [TODO: UPDATE once completed]

6. The script **plot_volcano_clustered_timeseries_plot.png** creates four subplots:

    - subplot(0,0) and subplot (0,1) will be the same. (Plot A)
    - subplot(1,0) and subplot (1,1) will be (Plot C) and (Plot D)

    - Plot A: Classic Timeseries Line plot where:
        - x-axis = Date
        - y-axis = Global Temperature data (or anomoly, TBD)

    - Plot C: A stem plot of the data from Data2.csv
        - x-axis = Date (matching axis alighnent with subplot(0,0)
        - y-axis = inverted stem plot of mass_so2 from each volcano
        - colorscheme: latzones

    - Plot D: A stem plot of the data from Data3.csv
        - x-axis = Date (matching axis alighnent with subplot(0,1)
        - y-axis = Inverted stem plot of clustered eruptions
        - colorscheme: latzones (same legend as Plot B)


***Methods Included:***
- my_utils.py
    - **open_file** 'Opens a comma separated CSV file.'
   
    - **get_column** 'Returns an array of integers from the result_column where the query_value matches the value in the query_column.'
   
    - **identify_column** 'Identifies the query and result columns of interest if entered as an integer or a string and gives the index values of those columns.'
    
    - **check_plume_height** 'Opens a comma separated CSV file, calculates if the value in the first query column is greater than the value in the second query column and then adds a 'y' or 'n' to the outputted list'

- bin_utils.py
    - **get_bindex** 'given a value and a list of bin edges, returns the index of the bin the value should go in'

    - **add_column_csv** 'makes copy of the infile with a new last column added'

- cluster_eruptions.py
    - **bin_by_latzone** 'determines the latitude zone bin of the volcanos in the infile, and writes a new outfile that is a copy of the infile but with new column named latbin_zone at the end.'
    
    - **cluster_eruptions_geotemporal** TODO: ADD

    - **identify_volcano_size** 'Identifies and bins volcanos by size from time_cluster_info_file. The output clusters have info of latbin_zone, size_unit, and coverage_time.'


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
