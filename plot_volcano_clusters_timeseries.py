'''
File: plot_volcano_clusters_timeseries.py
Author: Margot Clyne
Date: Nov 8 2020

This script will create four subplots:

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

'''
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import argparse
import plot_lib
from datetime import date
matplotlib.use('Agg')
import pylab
from pylab import rcParams

def main():
    parser = plot_lib.get_args('Make a volcano cluster timeseries plots.')

    # add argparser for extras
    parser.add_argument('--title',
                        type=str,
                        help='plot title',
                        default='')

    parser.add_argument('--label_plotA',
                        type=str,
                        help='label of dataset source',
                        default='Thompson 2009')

    parser.add_argument('--x_column_list',
                        type=int,
                        nargs='+',
                        help='x_column index from infile for'
                             'plotA, plotB, plotC, plotD.'
                             'ex: 0 0 2 1',
                        required=True)

    parser.add_argument('--y_column_list',
                        type=int,
                        nargs='+',
                        help='y_column index from infile for'
                             'plotA, plotB, plotC, plotD.'
                             'ex: 1 1 1 3',
                        required=True)

    # Plot C args
    parser.add_argument('--lat_bin_edges',
                        type=str,  # NOTE: or is it type int?
                        nargs='+',
                        help='list of lattitude bin edges',
                        required=True)

    parser.add_argument('--in_file_plotC',
                        type=str,
                        help='file name of un-clustered plotC data',
                        default=None)

    parser.add_argument('--latbins_column_list',
                        type=int,
                        nargs='+',
                        help='latbins_column index from infile for'
                             'plotC, plotD.'
                             'ex: 3 4',
                        required=True)

    # Plot D args
    parser.add_argument('--in_file_plotD',
                        type=str,
                        help='file name of clustered plotD data',
                        default=None)

    args = parser.parse_args()
    # All plots args
    outfile = args.out_file
    title = args.title
    x_label = args.x_label
    x_column_list = args.x_column_list
    y_column_list = args.y_column_list
    # Plot A (and B) args
    y_label_plotA = args.y_label
    infile_plotA = args.in_file
    label_plotA = args.label_plotA
    # Plot C (and some for D) args
    infile_plotC = args.in_file_plotC
    latbins_column_list = args.latbins_column_list
    lat_bin_edges = args.lat_bin_edges
    # Plot D args
    infile_plotD = args.in_file_plotD

    # calculate num_latbins and latzone_labels
    num_latbins = len(lat_bin_edges) - 1
    latzone_labels = []
    for z in range(1, num_latbins + 1):
        latzone_labels.append('latzone' + str(z) + ' [' + str(lat_bin_edges[z-1])
                              + ',' + str(lat_bin_edges[z]) + ')')

    lat_bin_list = range(1, num_latbins + 1)

    # load in all the data from each of the files
    x_columnA = x_column_list[0]
    y_columnA = y_column_list[0]
    x_columnC = x_column_list[2]
    y_columnC = y_column_list[2]
    x_columnD = x_column_list[3]
    y_columnD = y_column_list[3]
    latbins_columnC = latbins_column_list[0]
    latbins_columnD = latbins_column_list[1]

    # plot A data
    x_plotA = []
    y_plotA = []
    for line in open(infile_plotA):
        A = line.rstrip().strip("\ufeff").split(',')
        x_plotA.append(A[x_columnA])
        y_plotA.append(A[y_columnA])

    x_plotA = [date.fromisoformat(i) for i in x_plotA]
    y_plotA = [float(i) for i in y_plotA]
    
    # plot c data
    x_plotC = []
    y_plotC = []
    for z in range(num_latbins):
        data = get_column_localfunc(infile_plotC,
                                    latbins_columnC,
                                    str(lat_bin_list[z]),
                                    result_columns=[x_columnC, y_columnC])
        data[0] = [date.fromisoformat(i) for i in data[0]]
        data[1] = [float(i) for i in data[1]]
        x_plotC.append([data[0]])
        y_plotC.append([data[1]])
    
    # plot D data
    x_plotD = []
    y_plotD = []
    for z in range(num_latbins):
        data = get_column_localfunc(infile_plotD,
                                    latbins_columnD,
                                    str(lat_bin_list[z]),
                                    result_columns=[x_columnD, y_columnD])
        data[0] = [date.fromisoformat(i) for i in data[0]]
        data[1] = [float(i) for i in data[1]]
        x_plotD.append([data[0]])
        y_plotD.append([data[1]])

    # make plot
    rcParams['figure.figsize'] = (args.width, args.height)
    fig, ax = plt.subplots(2, 2)

    # add colormap and define latzone labels
    colormap = plt.cm.gist_ncar
    latzone_colors = colormap(np.linspace(0, 0.9, len(latzone_labels)))

    # SubplotA, B
    for j in range(0, 2):
        ax[0, j].plot(x_plotA, y_plotA, '-', color='blue', lw=2.0,
                      label=label_plotA)
        ax[0, j].set_ylim([-0.35, 0.])
        ax[0, j].set_ylabel(y_label_plotA)
        ax[0, j].spines['top'].set_visible(False)
        ax[0, j].spines['right'].set_visible(False)
        ax[0, j].legend()

    # SubplotC
    y_min_plotC = 0
    ax[1, 0].invert_yaxis()
    for z in range(num_latbins):
        if len(x_plotC[z][0])!= 0:
            markerlineC, stemlinesC, baselineC = \
                ax[1, 0].stem(x_plotC[z][0], y_plotC[z][0], linefmt='grey',
                              bottom=y_min_plotC, use_line_collection=True,
                              label=latzone_labels[z])
            markerlineC.set_markerfacecolor(latzone_colors[z])

    ax[1, 0].set_ylabel('Mass SO2 (kt)')
    ax[1, 0].xaxis.set_label_position('top')
    ax[1, 0].spines['top'].set_visible(False)
    ax[1, 0].spines['right'].set_visible(False)
    ax[1, 0].legend()

    # SubplotD
    ax[1, 1].invert_yaxis()
    for z in range(num_latbins):
        if len(x_plotD[z][0])!= 0:
            markerlineD, stemlinesD, baselineD = \
                ax[1, 1].stem(x_plotD[z][0], y_plotD[z][0],
                              linefmt='black',
                              bottom=y_min_plotC,
                              use_line_collection=True,
                            label=latzone_labels[z])
            markerlineD.set_markerfacecolor(latzone_colors[z])

    ax[1, 1].set_ylabel('Clustered Mass SO2 (kt)')
    ax[1, 1].xaxis.set_label_position('top')
    ax[1, 1].spines['top'].set_visible(False)
    ax[1, 1].spines['right'].set_visible(False)
    ax[1, 1].legend()

    # save file
    plt.show()
    plt.savefig(outfile, bbox_inches='tight', dpi=500)


def get_column_localfunc(file_name, query_column, query_value,
                         result_columns=[1], date_column=None,
                         return_dates=False):
    ''' Reads a CSV file and outputs the values of the results corresponding
        to the lines in which the query value is met

        Required imports:
        ---------
        array

        Parameters
        ----------
        file_name - string
                    name of the CSV file(including path if needed)

        query_column - int
                    index number of column query in CSV file

        query_value - string
                    the desired value to flter the query_column by

        results_columns - list of int
                    index numbers of columns results in CSV file

        Returns
        ---------
        hits - list of list of int
                    Values from results columns filtered by lines that
                    have the query_value gaps in dates are filled in
    '''
    # open and read file
    f = open(file_name, 'r', encoding='ISO-8859-1')
    hits = []
    for result_column in result_columns:
        hits.append([])
    for line in f:
        A = line.rstrip().split(',')
        # filter by where query_value is met
        if A[query_column] == query_value:
            for ind in np.arange(len(result_columns)):
                hits[ind].append(A[result_columns[ind]])

    f.close()
    return hits


if __name__ == '__main__':
    main()
