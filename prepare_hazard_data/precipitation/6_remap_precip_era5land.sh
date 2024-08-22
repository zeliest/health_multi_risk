#!/bin/bash

# Read directories and files from arguments passed by the main script
DATA_DIR="$1"
EXTREME_PRECIP_DIR="$2"
REMAP_OUTPUT_DIR="$3"
SOURCE_GRID="$4"
TARGET_GRID="$5"

# Create output directory if it doesn't exist
mkdir -p "$REMAP_OUTPUT_DIR"

# Create source and target grid description files
cat <<EOT > "$SOURCE_GRID"
gridtype = lonlat
gridsize = 6483600
xname = lon
xlongname = "Longitude"
xunits = "degrees_east"
yname = lat
ylongname = "Latitude"
yunits = "degrees_north"
xsize = 3600
ysize = 1801
xfirst = 0.05
xinc = 0.1
yfirst = -90.0
yinc = 0.1
EOT

cat <<EOT > "$TARGET_GRID"
gridtype = lonlat
gridsize = 1038240
xname = lon
xlongname = "Longitude"
xunits = "degrees_east"
yname = lat
ylongname = "Latitude"
yunits = "degrees_north"
xsize = 1440
ysize = 721
xfirst = 0.125
xinc = 0.25
yfirst = -90.0
yinc = 0.25
EOT

# Process each year
for year in $(seq 2000 2022); do
    INPUT_FILE="${EXTREME_PRECIP_DIR}/threshold_precip_99_9p_era5land_${year}.nc"
    TEMP_FILE="${EXTREME_PRECIP_DIR}/threshold_precip_99_9p_era5land_no_nan_${year}.nc"
    OUTPUT_FILE="${REMAP_OUTPUT_DIR}/threshold_precip_99_9p_era5land_remapped_0.25_${year}.nc"
    
    # Set NaNs to 0
    cdo setmisstoc,0 "$INPUT_FILE" "$TEMP_FILE"
    
    # Perform conservative remap on the thresholded data and save directly to the final output file
    cdo remapcon,"$TARGET_GRID" "$TEMP_FILE" "$OUTPUT_FILE"
    
    # Clean up temporary file
    rm "$TEMP_FILE"
    
    echo "Processed year ${year}"
done

# Remove all temporary files
rm ${EXTREME_PRECIP_DIR}/threshold_precip_era5land_no_nan_*.nc

echo "Regridding and fraction calculation completed."
