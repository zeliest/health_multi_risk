#!/bin/bash

# Define base directories
BASE_OUTPUT_DIR="/nfs/n2o/wcr/szelie/health_multi_risk_data/extreme_precip"
DATA_DIR="/nfs/atmos/data/era5-land_cds/processed/v1/tp/day/native"

# Define subdirectories based on the base directory
TEMP_DIR="${BASE_OUTPUT_DIR}/temp_chunks"
OUTPUT_DIR="${BASE_OUTPUT_DIR}/processed"
FILTERED_DIR="${BASE_OUTPUT_DIR}/filtered"
REMAP_OUTPUT_DIR="${BASE_OUTPUT_DIR}/remapped"
MONTHLY_MAX_OUTPUT_DIR="${BASE_OUTPUT_DIR}/monthly_max"

# Function to create directories if they do not exist
create_directories() {
    mkdir -p "$TEMP_DIR"
    mkdir -p "$OUTPUT_DIR"
    mkdir -p "$FILTERED_DIR"
    mkdir -p "$REMAP_OUTPUT_DIR"
    mkdir -p "$MONTHLY_MAX_OUTPUT_DIR"
}

# Function to print the status with a message
print_status() {
    echo -e "\n====================================="
    echo "Running: $1"
    echo "Description: $2"
    echo -e "=====================================\n"
}

# Create directories
create_directories

# Run each script with a description and pass the directory variables
print_status "1_chunk_files.sh" "Chunking climate data files by latitude and longitude for 1970-2000..."
./1_chunk_files.sh "$DATA_DIR" "$TEMP_DIR"
if [ $? -ne 0 ]; then
    echo "Script 1_chunk_files.sh failed with exit code $?. Exiting."
    exit 1
fi

print_status "2_concat_files.sh" "Concatenating chunked files along the time dimension..."
./2_concat_files.sh "$TEMP_DIR" "$TEMP_DIR"
if [ $? -ne 0 ]; then
    echo "Script 2_concat_files.sh failed with exit code $?. Exiting."
    exit 1
fi

print_status "3_calc_percentiles.sh" "Calculating the 99.9th percentiles for each grid point..."
./3_calc_percentiles.sh "$TEMP_DIR" "${BASE_OUTPUT_DIR}/percentiles"
if [ $? -ne 0 ]; then
    echo "Script 3_calc_percentiles.sh failed with exit code $?. Exiting."
    exit 1
fi

print_status "4_merge_percentiles.sh" "Merging calculated percentiles into a single dataset..."
./4_merge_percentiles.sh "${BASE_OUTPUT_DIR}/percentiles"
if [ $? -ne 0 ]; then
    echo "Script 4_merge_percentiles.sh failed with exit code $?. Exiting."
    exit 1
fi

print_status "5_values_above_percentile.sh" "Identifying and saving data values above the 99.9th percentile for 2003-2021..."
./5_values_above_percentile.sh "$DATA_DIR" "${BASE_OUTPUT_DIR}/percentiles/percentile_99_9_era5land_1970_2000_cleaned.nc" "$FILTERED_DIR"
if [ $? -ne 0 ]; then
    echo "Script 5_values_above_percentile.sh failed with exit code $?. Exiting."
    exit 1
fi

print_status "6_remap_precip_era5land.sh" "Remapping data to a 0.25-degree spatial resolution..."
./6_remap_precip_era5land.sh "$DATA_DIR" "$BASE_OUTPUT_DIR" "$REMAP_OUTPUT_DIR" "source_grid.txt" "target_grid.txt"
if [ $? -ne 0 ]; then
    echo "Script 6_remap_precip_era5land.sh failed with exit code $?. Exiting."
    exit 1
fi

print_status "7_calculate_monthly_max.sh" "Calculating monthly maximum values from the remapped data..."
./7_calculate_monthly_max.sh "$REMAP_OUTPUT_DIR" "$MONTHLY_MAX_OUTPUT_DIR"
if [ $? -ne 0 ]; then
    echo "Script 7_calculate_monthly_max.sh failed with exit code $?. Exiting."
    exit 1
fi

echo -e "\nAll scripts executed successfully."
