#!/bin/bash

# Define directories
OUTPUT_DIR="/nfs/n2o/wcr/szelie/health_multi_risk_data/extreme_precip/percentiles"
FINAL_OUTPUT="${OUTPUT_DIR}/percentile_99_9_era5land_1970_2000.nc"

# Merge all latitude percentile files into one
cdo collgrid "${OUTPUT_DIR}/percentile_99_9_lat*.nc" "$FINAL_OUTPUT"

