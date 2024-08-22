#!/bin/bash

# Define directories and files
EXTREME_PRECIP_DIR="/nfs/n2o/wcr/szelie/health_multi_risk_data/extreme_precip"
REMAP_OUTPUT_DIR="${EXTREME_PRECIP_DIR}"
MONTHLY_MAX_OUTPUT_DIR="${EXTREME_PRECIP_DIR}/monthly_max"

# Create output directories if they don't exist
mkdir -p "$MONTHLY_MAX_OUTPUT_DIR"

# Process each regridded file
for year in $(seq 2000 2022); do
    INPUT_FILE="${REMAP_OUTPUT_DIR}/threshold_precip_99_9p_era5land_remapped_0.25_${year}.nc"
    OUTPUT_FILE="${MONTHLY_MAX_OUTPUT_DIR}/thresholdprecip_99_9_era5land_remapped_0.25_monthly_max_${year}.nc"
    
    # Calculate the monthly maximum for each grid point
    cdo monmax "$INPUT_FILE" "$OUTPUT_FILE"
    
    echo "Processed monthly max for year ${year}"
done

echo "Monthly maximum calculation completed."

