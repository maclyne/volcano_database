test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest


# Calculate_strato_eruptions.py tests
rm -f 'Updated_data.csv'
run test_full_run_calculate_strato_eruptions python calculate_strato_eruptions.py \
            --file 'carn_MSVOLSO2L4_forclassproject.csv' \
            --query_columns "alt" "tropo" \
            --out_file 'Updated_data.csv'
assert_exit_code 0
assert_no_stderr
assert_equal 'Updated_data.csv' $( ls 'Updated_data.csv' )
assert_in_stdout "['y', 'y', 'y', 'n', 'n', 'y', 'y', 'y', 'n', 'y', 'y', 'y', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'y', 'y', 'y', 'y', 'n', 'y', 'y', 'n', 'n', 'n', 'y', 'y', 'n', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'n', 'y', 'y', 'y', 'n', 'n', 'y', 'y', 'n', 'y', 'y', 'n', 'n', 'n', 'n', 'n', 'n', 'y', 'n', 'n', 'y', 'n', 'y', 'n', 'n', 'n', 'n', 'y', 'n', 'n', 'n', 'n', 'n', 'y', 'y', 'y', 'n', 'n', 'n', 'y', 'n', 'n', 'y', 'n', 'n', 'n', 'y', 'y', 'y', 'n', 'y', 'n', 'y', 'y', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'y', 'y', 'y', 'y', 'n', 'n', 'y', 'y', 'n', 'n', 'n', 'n', 'y', 'y', 'y', 'n', 'y', 'y', 'n', 'n', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'y', 'y', 'y', 'y', 'n', 'n', 'y', 'y', 'y', 'y', 'y', 'y', 'n', 'n', 'y', 'n', 'n', 'y', 'y', 'y', 'n', 'n', 'n', 'y', 'y', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'y', 'n', 'y', 'y']"


# extract_eruptions.py tests
rm -f 'Data1.csv'
run test_full_run_extract_eruptions python extract_eruptions.py \
            --file 'Updated_data.csv' \
            --query_column "Stratospheric_(y/n)" \
            --query "y" \
            --result_columns "ï»¿volcano" "date" "lat" "so2(kt)"\
            --out_file 'Data1.csv'
assert_no_stdout
assert_no_stderr
assert_exit_code 0
assert_equal 'Data1.csv' $( ls 'Data1.csv' )


# cluster_eruptions.py tests
LAT_BIN_EDGES=$(cat 'lat_bin_edges_file.txt' | xargs printf "%s" | awk -F',' '{{gsub(" ","-"); print}}' | awk -F',' '{{gsub(","," "); print}}' | sed 's/[][]//g')
rm -f 'Data2.csv'
run test_full_run_bin_by_latzone python cluster_eruptions.py \
            --function_name "bin_by_latzone" \
            --infile 'Data1.csv' \
            --outfile 'Data2.csv' \
            -lat_column 2 \
            -lat_bin_edges $LAT_BIN_EDGES 
assert_no_stdout
assert_no_stderr
assert_exit_code 0
assert_equal 'Data2.csv' $( ls 'Data2.csv' )

rm -f 'Data3.csv'
run test_full_run_identify_volcano_size python cluster_eruptions.py \
            --function_name 'identify_volcano_size' \
            --infile 'Data2.csv' \
            --outfile 'Data3.csv' \
            -SO2_output_column 3 \
            -time_cluster_info_file 'time_cluster_info_file.csv'
assert_no_stdout
assert_no_stderr
assert_exit_code 0
assert_equal 'Data3.csv' $( ls 'Data3.csv' )