#!/bin/bash

# Read directories from arguments passed by the main script
EXTREME_PRECIP_DIR="$1"
MONTHLY_MAX_OUTPUT_DIR="$2"

# Create output directory if it doesn't exist
mkdir -p "$MONTHLY_MAX_OUTPUT_DIR"

# Process each year
for year in $(seq 2000 2022); do
    INPUT_FILE="${EXTREME_PRECIP_DIR}/threshold_precip_99_9p_era5land_remapped_0.25_${year}.nc"
    OUTPUT_FILE="${MONTHLY_MAX_OUTPUT_DIR}/monthly_max_precip_99_9p_era5land_remapped_0.25_${year}.nc"
    
    # Check if the input file exists
    if [[ -f "$INPUT_FILE" ]]; then
        # Calculate monthly maximum values
        cdo timmax "$INPUT_FILE" "$OUTPUT_FILE"
        
        echo "Processed monthly max for year ${year}"
    else
        echo "Input file ${INPUT_FILE} does not exist!"
    fi
done

echo "Monthly maximum calculation completed."
