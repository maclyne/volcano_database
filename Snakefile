rule all:
	input: 'volcano_clustered_timeseries_plot.png'

rule update_input_Data_file:
    input: 'carn_MSVOLSO2L4_forclassproject.csv'
    output: 'Updated_data.csv'
    shell: 
        '''
        python calculate_strato_eruptions.py \
            --file {input} \
            --query_columns "alt" "tropo" \
            --out_file {output}
        '''

rule create_Data1_file:
    input: 'Updated_data.csv'
    output: 'Data1.csv'
    shell: 
        '''
        python extract_eruptions.py \
            --file {input} \
            --query_column "Stratospheric_(y/n)" \
            --query "y" \
            --result_columns "ï»¿volcano" "date" "lat" "so2(kt)"\
            --out_file {output}
        # creates outputfile Data1.csv with columns of: 
                   # volcano_label, date, latitude, mass_so2
                   # NOTE: for ONLY stratospheric eruptions
        '''

rule create_Data2_file:
    input: 'Data1.csv', 'lat_bin_edges_file.txt'
    output: 'Data2.csv'
    shell: 
        '''
        LAT_BIN_EDGES=$(cat {input[1]} | xargs printf "%s" | awk -F',' '{{gsub(" ","-"); print}}' | awk -F',' '{{gsub(","," "); print}}' | sed 's/[][]//g')

        python cluster_eruptions.py \
            --function_name "bin_by_latzone" \
            --infile {input[0]} \
            --outfile {output} \
            -lat_column 2 \
            -lat_bin_edges $LAT_BIN_EDGES 
        '''

rule identify_volcano_size:
    input: 'Data2.csv', 'time_cluster_info_file.csv'
    output: 'Data3.csv'
    shell:
        '''
        python cluster_eruptions.py \
            --function_name 'identify_volcano_size' \
            --infile {input[0]} \
            --outfile {output} \
            -SO2_output_column 3 \
            -time_cluster_info_file {input[1]}
            # creates outputfile Data3.csv with columns of: 
                   # volcano_label, date, latitude, mass_so2, latbin_zone, size_unit, and coverage_time_years
        '''

rule create_Data4_file:
    input: 'Data3.csv'
    output: 'Data4.csv'
    shell:     #NOTE: (TODO) this will create Data4.csv with columns of: lat_bin_number, binned_mass_so2, binned_date
        '''
        python cluster_eruptions.py \
            --function_name 'cluster_eruptions_geotemporal' \
            # TODO: add rest of arguments
        '''

rule timeseries_plots:
    input: 'Data2.csv', 'Data4.csv', 'volcano_sig_Thompson2009.csv'
    output: 'volcano_clustered_timeseries_plot.png'
    shell: 
        '''
        python plot_volcano_clusters_timeseries.py \
            --in_file 'volcano_sig_Thompson2009.csv' \
                    --out_file {output} \
                    --x_label 'Date' \
                    --y_label 'Volcano fit anomoly of global mean SST' \
                    --height 5 \
                    --width 5 \
                    --title 'Stratospheric Volcanic Eruptions' \
            --label_plotA 'Thompson 2009' \
            --x_column_list #TODO \ 
            --y_column_list #TODO \
            --lat_bin_edges $LAT_BIN_EDGES \
            --in_file_plotC 'Data2.csv' \
            --latbins_column_list #TODO \
            --in_file_plotD 'Data3.csv'
        '''

