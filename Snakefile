rule all:
	input: 'volcano_clustered_timeseries_plot.png'

rule create_Data1_file:
	input: 'Aubry_2017_Table_S2_database_volcano_parameters.csv'
	output: 'Data1.csv'
	shell:
	'''
	# python stuff that creates outputfile Data1.csv with columns of: 
               volcano_label, lattitude, date, mass_so2
               # NOTE: for ONLY stratospheric eruptions
	'''

rule create_Data2_file:
	input: 'Data1.csv', 'lat_bin_edges_file.txt'
	output: 'Data2.csv'
	shell:
	'''
	LAT_BIN_EDGES=$(cat lat_bin_edges_file.txt | xargs printf "%s" | awk -F',' '{{gsub(" ","-"); print}}' | awk -F',' '{{gsub(","," "); print}}' | sed 's/[][]//g')
	
	python cluster_eruptions.py \
		--function_name 'bin_by_latzone' \
		--infile 'Data1.csv' \
		--outfile {output} \
		--lat_column 1 \ 			#NOTE: idk what the actual lat_column is from Data1.csv
		--lat_bin_edges $LAT_BIN_EDGES 
	'''

rule create_Data3_file:
	input: 'Data2.csv'
	output: 'Data3.csv'
	shell:     #NOTE: (TODO) this will create Data3.csv with columns of: lat_bin_number, binned_mass_so2, binned_date
	'''
	python cluster_eruptions.py \
		--function_name 'cluster_eruptions_geotemporal' \
		# TODO: add rest of arguments
	'''

rule timeseries_plots:
	input: 'Data2.csv', 'Data3.csv', 'volcano_sig_Thompson2009.csv'
	output: 'volcano_clustered_timeseries_plot.png'
	shell:
	'''
	# TODO
	'''

