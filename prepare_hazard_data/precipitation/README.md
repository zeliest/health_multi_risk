Scripts

the script "generate_precip_data.sh" runs all the following scrpts:

1. 1_chunk_files.sh
Purpose:
This script chunks the climate data files by latitude and longitude for 1970-2000. Chunking is done to manage the large datasets more efficiently by breaking them down into smaller, more manageable pieces.

Actions:

Reads input data files.
Splits these files into chunks based on specified latitude and longitude ranges.

2. 2_concat_files.sh
Purpose:
This script concatenates the chunked files along the time dimension. This step is necessary to create a continuous time series from the spatially chunked data to caclulate percentiles .

Actions:

Takes the chunked files created by 1_chunk_files.sh.
Merges these files along the time axis to create a complete time series for each spatial chunk.

3. 3_calc_percentiles.sh
Purpose:
This script calculates the 99.9 percentiles for each latitude/longitude box in the dataset. 

Actions:

Reads the concatenated files from 2_concat_files.sh.
Calculates percentile (99.9th) for each grid point.

4. 4_merge_percentiles.sh
Purpose:
This script merges the calculated percentiles into a single dataset. Merging is necessary to combine the percentile information across all spatial chunks.

Actions:

Takes the percentile data calculated by 3_calc_percentiles.sh.
Merges these percentile values into a unified dataset.

5. 5_values_above_percentile.sh
Purpose:
This script identifies and saves the data values for total precipitation 2003-2021 that are above a specified percentile threshold. This step is useful for identifying extreme values or events in the dataset.

Actions:

Reads the merged percentiles from 4_merge_percentiles.sh.
Extracts and saves values that exceed a specified percentile threshold (e.g., 99.9th percentile).

6. 6_remap_precip_era5land.sh
Purpose:
This script remaps the data to a 0.25 spatial resolution by savind the fraction that is above the 99.9th percentile for each time step at each grid cell

Actions:

Takes the values above the percentile threshold from 5_values_above_percentile.sh.
Remaps these values to a new spatial resolution (e.g., 0.25 degrees).

7. 7_calculate_monthly_max.sh
Purpose:
This script calculates the monthly maximum values for the remapped data. 

Actions:

Reads the remapped data resulting from 6_remap_precip_era5land.sh.
Calculates the maximum value for each month.
Saves these monthly maximum values to the output files.


Supporting Files

source_grid.txt
Description:
This file contains the grid information for the source data. It includes details such as the grid resolution and the latitude/longitude bounds.

target_grid.txt
Description:
This file contains the grid information for the target data. It specifies the new grid resolution and the latitude/longitude bounds for remapping the data.