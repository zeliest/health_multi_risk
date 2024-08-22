#!/bin/bash

# Define directories
TEMP_DIR="/nfs/n2o/wcr/szelie/health_multi_risk_data/temp_chunks"
OUTPUT_DIR="/nfs/n2o/wcr/szelie/health_multi_risk_data/extreme_precip/percentiles"
LAT_CHUNK_SIZE=6  # Chunk size in degrees

# Define latitude bounds for splitting
LAT_BOUNDS=($(seq -90 $LAT_CHUNK_SIZE 90))

# Function to calculate percentiles
calculate_percentiles() {
    local lat_start=$1
    local lat_end=$2
    local merged_file="${TEMP_DIR}/merged_lat${lat_start}-${lat_end}.nc"
    local output_file="${OUTPUT_DIR}/percentile_99_9_lat${lat_start}-${lat_end}.nc"

    # Check if the merged file exists
    if [[ -f "$merged_file" ]]; then
        # Use cdo to calculate the 99th percentile
        cdo timpctl,99.9 "$merged_file" -timmin "$merged_file" -timmax "$merged_file" "$output_file"
    else
        echo "Merged file ${merged_file} does not exist!"
    fi
}

# Loop through each latitude chunk and calculate percentiles
for i in "${!LAT_BOUNDS[@]}"; do
    if [ $i -lt $((${#LAT_BOUNDS[@]}-1)) ]; then
        lat_start=${LAT_BOUNDS[$i]}
        lat_end=${LAT_BOUNDS[$((i+1))]}
        calculate_percentiles $lat_start $lat_end
    fi
done

