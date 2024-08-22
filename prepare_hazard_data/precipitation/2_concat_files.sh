#!/bin/bash

# Read directories from arguments passed by the main script
TEMP_DIR="$1"
OUTPUT_DIR="$2"
LAT_CHUNK_SIZE=6  # Chunk size in degrees

# Define latitude bounds for merging
LAT_BOUNDS=($(seq -90 $LAT_CHUNK_SIZE 90))

# Function to merge latitude chunks for each time period
merge_chunks() {
    local lat_start=$1
    local lat_end=$2
    local temp_file="${OUTPUT_DIR}/merged_lat${lat_start}-${lat_end}.nc"

    cdo mergetime "${TEMP_DIR}/tp_day_era5-land_*_lat${lat_start}-${lat_end}.nc" "$temp_file"
}

# Loop through each latitude chunk and merge
for i in "${!LAT_BOUNDS[@]}"; do
    if [ $i -lt $((${#LAT_BOUNDS[@]}-1)) ]; then
        lat_start=${LAT_BOUNDS[$i]}
        lat_end=${LAT_BOUNDS[$((i+1}))}
        merge_chunks $lat_start $lat_end
    fi
done