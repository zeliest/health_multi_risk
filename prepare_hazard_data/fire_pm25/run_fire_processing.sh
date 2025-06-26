#!/bin/bash

# Base directory for fire data
BASE_FIRE_DIR="/nfs/n2o/wcr/szelie/health_multi_risk_data/hazard_input_data/fire_pm25"
REMAPPED_DIR="${BASE_FIRE_DIR}/remapped"
MONTHLY_REMAPPED_DIR="${BASE_FIRE_DIR}/remapped_monthly"
TARGET_GRID="/nfs/n2o/wcr/szelie/health_multi_risk_data/hazard_input_data/extreme_precip/monthly_max/monthly_max_precip_99_9p_era5land_remapped_0.25_2022.nc"

# Export these directories as environment variables to be used by processing scripts
export FIRE_DIR=$BASE_FIRE_DIR
export REMAPPED_DIR=$REMAPPED_DIR
export MONTHLY_REMAPPED_DIR=$MONTHLY_REMAPPED_DIR
export TARGET_GRID=$TARGET_GRID

# Run the regridding script
./1_cdo_script_remap_fire.sh "$FIRE_DIR" "$REMAPPED_DIR" "$TARGET_GRID"

# Check if regridding was successful
if [ $? -eq 0 ]; then
    echo "Regridding completed successfully. Proceeding to process fire data..."
    
    # Run the monthly max processing script
    ./2_cdo_script_monthly_max_fire.sh "$REMAPPED_DIR" "$MONTHLY_REMAPPED_DIR"
else
    echo "Regridding failed. Aborting further processing."
    exit 1
fi