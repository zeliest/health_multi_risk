#!/bin/bash

# Accept input parameters
FIRE_DIR="$1"         # First argument: base directory for fire data
REMAPPED_DIR="$2"     # Second argument: output directory for remapped data
TARGET_GRID="$3"      # Third argument: path to target grid file

# Set default values if not provided
FIRE_DIR="${FIRE_DIR:-/default/path/to/fire_pm25}"
REMAPPED_DIR="${REMAPPED_DIR:-/default/path/to/fire_pm25/remapped}"
TARGET_GRID="${TARGET_GRID:-/default/path/to/target_grid.nc}"

# Create remapped directory if it doesn't exist
mkdir -p $REMAPPED_DIR

# Loop through the years 2003 to 2022 (or customize the year range)
for YEAR in {2003..2021}; do
  # Define the filenames for fire data and output for remapping
  FIRE_FILE="${FIRE_DIR}/globPMfire02deg_${YEAR}.nc4"
  OUTPUT_FILE="${REMAPPED_DIR}/globPMfire_remapped_025deg_${YEAR}.nc"

  # Check if the fire data file exists before attempting to regrid
  if [[ -f "$FIRE_FILE" ]]; then
    echo "Regridding fire data for ${YEAR}..."
    
    # Perform the regridding using bilinear interpolation
    cdo remapbil,"$TARGET_GRID" "$FIRE_FILE" "$OUTPUT_FILE"
    
    if [ $? -eq 0 ]; then
      echo "Regridding completed successfully for ${YEAR}"
    else
      echo "Error occurred during regridding for ${YEAR}"
    fi
  else
    echo "Fire data file missing for ${YEAR}: ${FIRE_FILE}. Skipping..."
  fi
done

echo "Regridding operations completed for all years."