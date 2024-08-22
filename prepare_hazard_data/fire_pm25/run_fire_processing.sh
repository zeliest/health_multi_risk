#!/bin/bash

# Set the base directory for the fire data and remapped output
BASE_FIRE_DIR="/nfs/n2o/wcr/szelie/health_multi_risk_data/fire_pm25"
REMAPPED_DIR="${BASE_FIRE_DIR}/remapped"

# Pass these directories as environment variables to the individual scripts
export FIRE_DIR=$BASE_FIRE_DIR
export REMAPPED_DIR=$REMAPPED_DIR

# Run the regridding script
./regrid_fire.sh

# Check if regridding was successful
if [ $? -eq 0 ]; then
    echo "Regridding completed successfully. Proceeding to process fire data..."
    # Run the processing script
    ./process_fire.sh
else
    echo "Regridding failed. Aborting further processing."
    exit 1
fi
