#!/bin/bash

# Define directories
DATA_DIR="/nfs/atmos/data/era5-land_cds/processed/v1/tp/day/native"
TEMP_DIR="/nfs/n2o/wcr/szelie/health_multi_risk_data/temp_chunks"
OUTPUT_DIR="/nfs/n2o/wcr/szelie/health_multi_risk_data/extreme_precip"
START_YEAR=1980
END_YEAR=1990
LAT_CHUNK_SIZE=6  # Chunk size in degrees

mkdir -p "$TEMP_DIR"
mkdir -p "$OUTPUT_DIR"

# Define latitude bounds for splitting
LAT_BOUNDS=($(seq -90 $LAT_CHUNK_SIZE 90))

# Function to chunk files by latitude
chunk_file() {
    local year=$1
    local lat_start=$2
    local lat_end=$3
    local temp_file="${TEMP_DIR}/tp_day_era5-land_${year}_lat${lat_start}-${lat_end}.nc"
    
    cdo sellonlatbox,0,360,${lat_start},${lat_end} "${DATA_DIR}/tp_day_era5-land_${year}.nc" "$temp_file"
}

# Loop through each year and each latitude chunk
for year in $(seq $START_YEAR $END_YEAR); do
    for i in "${!LAT_BOUNDS[@]}"; do
        if [ $i -lt $((${#LAT_BOUNDS[@]}-1)) ]; then
            lat_start=${LAT_BOUNDS[$i]}
            lat_end=${LAT_BOUNDS[$((i+1))]}
            chunk_file $year $lat_start $lat_end
        fi
    done
done

