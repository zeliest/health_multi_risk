#!/bin/bash

# Define directories and input/output files based on the known paths
cd "/Users/szelie/OneDrive - ETH Zurich/data/health_multi_risk_data"
TEST_DATA_DIR="test_data"   # Path to test data directory
TEMP_OUTPUT_DIR="${TEST_DATA_DIR}/temp_output"     # Temporary output directory inside test_data
TARGET_GRID_FILE="${TEST_DATA_DIR}/target_grid.txt"  # Path to target grid file

# Ensure the temporary output directory exists
mkdir -p "$TEMP_OUTPUT_DIR"

# Loop through years (you can adjust the range as needed)
for YEAR in {2004}; do
    INPUT_FILE="${TEST_DATA_DIR}/globPMfire02deg_${YEAR}.nc4"
    REMAP_OUTPUT_FILE="${TEMP_OUTPUT_DIR}/globPMfire_remapped_025deg_${YEAR}.nc"
    MONTHLY_MAX_OUTPUT_FILE="${TEMP_OUTPUT_DIR}/globPMfire_monthly_max_025deg_${YEAR}.nc"

    # Check if the input file exists
    if [[ -f "$INPUT_FILE" ]]; then
        echo "Running remap for year ${YEAR}..."

        # Remap using bilinear interpolation
        cdo remapbil,"$TARGET_GRID_FILE" "$INPUT_FILE" "$REMAP_OUTPUT_FILE"

        if [[ $? -eq 0 ]]; then
            echo "Remapping successful for year ${YEAR}. Calculating monthly max..."

            # Calculate the monthly maximum
            cdo monmax "$REMAP_OUTPUT_FILE" "$MONTHLY_MAX_OUTPUT_FILE"

            if [[ $? -eq 0 ]]; then
                echo "Monthly max calculated successfully for year ${YEAR}."
            else
                echo "Error: Monthly max calculation failed for year ${YEAR}."
            fi
        else
            echo "Error: Remapping failed for year ${YEAR}."
        fi
    else
        echo "Input file ${INPUT_FILE} not found. Skipping year ${YEAR}."
    fi
done

echo "Processing completed. Check outputs in ${TEMP_OUTPUT_DIR}."

cd "/Users/szelie/python_projects/health_multi_risk/tests"
pytest tests_fire_pm25.py -v
