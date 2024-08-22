#!/bin/bash

# Read directory from argument passed by the main script
OUTPUT_DIR="$1"
FINAL_OUTPUT="${OUTPUT_DIR}/percentile_99_9_era5land_1970_2000.nc"

# Merge all latitude percentile files into one
cdo collgrid "${OUTPUT_DIR}/percentile_99_9_lat*.nc" "$FINAL_OUTPUT"
