## Fire Data Processing

In this folder, we used **CDO (Climate Data Operators)** to process the fire-related data.

The main script is:

- **`run_fire_processing.sh`**  
  This script orchestrates the workflow by calling the following two scripts in sequence:

  1. **`1_cdo_script_remap_fire.sh`**  
     This script remaps the original data from a 0.2° grid to a 0.25° grid.

  2. **`2_cdo_script_monthly_max_fire.sh`**  
     This script computes the **monthly maximum** values from the remapped data.
