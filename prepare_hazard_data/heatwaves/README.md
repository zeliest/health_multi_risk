## Folder Description

This folder is made up of three files:

1. **`download_and_process_era5_temperatures.py`**  
   A Python script that allows you to download the required ERA5 temperature data.

2. **`1_heatwaves_quantiles.ipynb`**  
   A Jupyter notebook that guides you through the calculation of quantiles based on the downloaded data.

3. **`2_heatwave_bymonth.ipynb`**  
   A notebook that uses the previously calculated quantiles to compute the number of days exceeding those thresholds — i.e., the heatwave days.
