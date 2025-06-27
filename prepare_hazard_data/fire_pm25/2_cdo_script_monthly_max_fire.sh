#!/bin/bash

# Use the directories set by the main script
REMAPPED_DIR="${REMAPPED_DIR:-/default/path/to/fire_pm25/remapped}"

# Loop through the years 2003 to 2022 for the second processing step
for YEAR in {2003..2021}
do
  # Define the filenames for the processed fire data
  INPUT_FILE="${REMAPPED_DIR}/globPMfire_remapped_025deg_${YEAR}.nc"
  MEAN_FILE="${MONTHLY_REMAPPED_DIR}/globPMfire_3day_mean_${YEAR}.nc"
  MAX_FILE="${MONTHLY_REMAPPED_DIR}/globPMfire_monthly_max_3day_mean_${YEAR}.nc"

  # Check if the regridded fire data file exists
  if [ -f "$INPUT_FILE" ]; then
    echo "Processing 3-day running mean and monthly max for ${YEAR}..."
    
    # Calculate the 3-day running mean
    cdo timselmean,3 $INPUT_FILE $MEAN_FILE
    
    # Calculate the monthly maximum from the 3-day running mean
    cdo monmax $MEAN_FILE $MAX_FILE

    # Optionally, remove the mean file if no longer needed
    rm $MEAN_FILE

    echo "Processed ${YEAR} successfully."
  else
    echo "Input file missing for ${YEAR}: Skipping..."
  fi
done

echo "All fire data processing completed."
#!/bin/bash

# Accept input parameters
REMAPPED_DIR="$1"             # First argument: remapped data directory
MONTHLY_REMAPPED_DIR="$2"     # Second argument: output directory for monthly max data

# Set default values if not provided
REMAPPED_DIR="${REMAPPED_DIR:-/default/path/to/fire_pm25/remapped}"
MONTHLY_REMAPPED_DIR="${MONTHLY_REMAPPED_DIR:-/default/path/to/fire_pm25/remapped_monthly}"

# Create monthly remapped directory if it doesn't exist
mkdir -p $MONTHLY_REMAPPED_DIR

# Loop through the years 2003 to 2022 (or customize the year range)
for YEAR in {2003..2021}; do
  # Define the filenames for the processed fire data
  INPUT_FILE="${REMAPPED_DIR}/globPMfire_remapped_025deg_${YEAR}.nc"
  MEAN_FILE="${MONTHLY_REMAPPED_DIR}/globPMfire_3day_mean_${YEAR}.nc"
  MAX_FILE="${MONTHLY_REMAPPED_DIR}/globPMfire_monthly_max_3day_mean_${YEAR}.nc"

  # Check if the regridded fire data file exists
  if [[ -f "$INPUT_FILE" ]]; then
    echo "Processing 3-day running mean and monthly max for ${YEAR}..."
    
    # Calculate the 3-day running mean
    cdo timselmean,3 "$INPUT_FILE" "$MEAN_FILE"
    
    # Calculate the monthly maximum from the 3-day running mean
    cdo monmax "$MEAN_FILE" "$MAX_FILE"

    # Optionally, remove the mean file if no longer needed
    rm "$MEAN_FILE"

    echo "Processed ${YEAR} successfully."
  else
    echo "Input file missing for ${YEAR}: Skipping..."
  fi
done

echo "All fire data processing completed."
