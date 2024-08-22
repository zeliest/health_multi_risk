#!/bin/bash

# Read directories and file paths from arguments passed by the main script
DATA_DIR="$1"
PERCENTILES_FILE="$2"
FILTERED_DIR="$3"

# Create the filtered directory if it doesn't exist
mkdir -p "$FILTERED_DIR"

# Function to filter data based on percentiles and set values above the threshold to 1
filter_data() {
    local year=$1
    local input_file="${DATA_DIR}/tp_day_era5-land_${year}.nc"
    local output_file="${FILTERED_DIR}/threshold_precip_99_9p_era5land_${year}.nc"
    local temp_file="${FILTERED_DIR}/temp_${year}.nc"

    # Check if the input file exists
    if [[ -f "$input_file" ]]; then
        # Subtract the percentile file from the input file
        cdo -L -sub "${input_file}" "${PERCENTILES_FILE}" "${temp_file}"
        
        # Create a binary mask: 1 for values greater than 0, 0 otherwise
        cdo -L -expr,'tp=(tp>0)?1:0' "${temp_file}" "${output_file}"

        # Clean up the temporary file
        rm "${temp_file}"
    else
        echo "Input file ${input_file} does not exist!"
    fi
}

# Loop through each year and filter data
for year in $(seq 2000 2022); do
    filter_data $year
done