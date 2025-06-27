import os
import netCDF4 as nc
import numpy as np
import sys
sys.path.insert(0, '..')
from config import DATA_DIR  # Import DATA_DIR from config.py

# Define the paths using the imported DATA_DIR from config.py
TEST_DATA_DIR = os.path.join(DATA_DIR, 'test_data')
TEMP_OUTPUT_DIR = os.path.join(TEST_DATA_DIR, 'temp_output')

# Define specific file paths
remapped_file = os.path.join(TEMP_OUTPUT_DIR, 'globPMfire_remapped_025deg_2004.nc')
monthly_max_file = os.path.join(TEMP_OUTPUT_DIR, 'globPMfire_monthly_max_025deg_2004.nc')

def test_remapped_file_exists():
    """Test if remapped file exists"""
    assert os.path.exists(remapped_file), f"Remapped file {remapped_file} does not exist."

def test_monthly_max_file_exists():
    """Test if monthly max file exists"""
    assert os.path.exists(monthly_max_file), f"Monthly max file {monthly_max_file} does not exist."

def test_fire_pm25_data():
    """Test basic statistics and value checks for the remapped file."""
    with nc.Dataset(remapped_file) as remapped_ds:
        fire_pm25_remapped = remapped_ds.variables['fire_pm25'][:]

        # Test 1: Check basic statistics of the remapped data
        assert fire_pm25_remapped.min() >= -1.0, f"Min value {fire_pm25_remapped.min()} is less than -1.0"
        assert fire_pm25_remapped.max() <= 1.0, f"Max value {fire_pm25_remapped.max()} is greater than 1.0"

        print(f"Min: {fire_pm25_remapped.min()}, Max: {fire_pm25_remapped.max()}, Mean: {fire_pm25_remapped.mean()}")

def test_specific_value_at_location():
    """Test a specific value at lat=0, lon=0, time=0."""
    with nc.Dataset(remapped_file) as remapped_ds:
        fire_pm25_remapped = remapped_ds.variables['fire_pm25'][:]
        lat = remapped_ds.variables['lat'][:]
        lon = remapped_ds.variables['lon'][:]

        # Find the index closest to lat=0, lon=0
        lat_idx = np.abs(lat - 0).argmin()
        lon_idx = np.abs(lon - 0).argmin()

        # Check the value for the first time step at lat=0, lon=0
        test_value = fire_pm25_remapped[0, lat_idx, lon_idx]
        expected_value = 0.0  # Change according to expected
        assert np.isclose(test_value, expected_value, atol=1e-3), \
            f"Value at lat=0, lon=0 is {test_value}, expected {expected_value}"

def test_monthly_max_values():
    """Test monthly maximum statistics."""
    with nc.Dataset(monthly_max_file) as monthly_max_ds:
        fire_pm25_monthly_max = monthly_max_ds.variables['fire_pm25'][:]

        # Test basic statistics
        print(f"Min: {fire_pm25_monthly_max.min()}, Max: {fire_pm25_monthly_max.max()}, Mean: {fire_pm25_monthly_max.mean()}")

