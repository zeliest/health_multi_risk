#!/bin/bash

# Define directories
TEMP_DIR="/nfs/n2o/wcr/szelie/health_multi_risk_data/temp_chunks"
OUTPUT_DIR="/nfs/n2o/wcr/szelie/health_multi_risk_data/extreme_precip"
LAT_CHUNK_SIZE=6  # Chunk size in degrees

# Define latitude bounds for splitting
LAT_BOUNDS=($(seq -90 $LAT_CHUNK_SIZE 90))

# Function to merge latitude chunks for each time period
merge_chunks() {
    local lat_start=$1
    local lat_end=$2
    local temp_file="${TEMP_DIR}/merged_lat${lat_start}-${lat_end}.nc"

    cdo mergetime "${TEMP_DIR}/tp_day_era5-land_*_lat${lat_start}-${lat_end}.nc" "$temp_file"
}

# Loop through each latitude chunk and merge
for i in "${!LAT_BOUNDS[@]}"; do
    if [ $i -lt $((${#LAT_BOUNDS[@]}-1)) ]; then
        lat_start=${LAT_BOUNDS[$i]}
        lat_end=${LAT_BOUNDS[$((i+1))]}
        merge_chunks $lat_start $lat_end
    fi
done

