from pathlib import Path
from climada.entity import Exposures
from climada.engine import Impact
import numpy as np
import sys
from shapely.geometry import Point

import xarray as xr
import pandas as pd
sys.path.insert(0, '..')
from config import DATA_DIR

# Define subdirectories relative to the base DATA_DIR
IMP_DIR = DATA_DIR / "impacts"
INPUT_DIR = DATA_DIR / "hazard_input_data"
EXPOSURES_DIR = DATA_DIR / "population/worldpop/climada_exposures"

def write_impact(impact, hazard_type, age):
    impact.write_csv(IMP_DIR / f"csv/{hazard_type}_{age}_2003_2022.csv")
    impact.write_sparse_csr(IMP_DIR / f"npz/{hazard_type}_{age}_2003_2022.npz")

def read_impact(hazard_type, age):
    impact = Impact.from_csv(IMP_DIR / f"csv/{hazard_type}_{age}_2003_2022.csv")
    impact.imp_mat = Impact.read_sparse_csr(IMP_DIR / f"npz/{hazard_type}_{age}_2003_2022.npz")
    return impact

def impact_from_netcdf(nc_path, haz_type='custom', unit='', frequency_unit='1/year'):
    """
    Recreate a simplified CLIMADA Impact object from a NetCDF containing just imp_mat data
    with dimensions (time, lat, lon) representing impact per month.

    Parameters
    ----------
    nc_path : str
        Path to NetCDF file.
    haz_type : str
        Hazard type string (e.g., 'heat').
    unit : str
        Unit of impact values (e.g., 'USD').
    frequency_unit : str
        Frequency unit string, e.g. '1/year'.

    Returns
    -------
    Impact
        Reconstructed CLIMADA Impact object.
    """
    ds = xr.open_dataset(nc_path).fillna(0)
    var_name = list(ds.data_vars)[0]
    imp_vals = ds[var_name].values  # shape: (time, lat, lon)
    times = ds.time.values
    lats = ds.latitude.values
    lons = ds.longitude.values

    # Flatten spatial grid
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    coord_exp = np.column_stack([lat_grid.ravel(), lon_grid.ravel()])  # (n_exp, 2)

    # Flatten impact values to shape (n_events, n_exp)
    imp_mat_dense = imp_vals.reshape(len(times), -1)  # (events, exposures)

    # Compute event-level and exposure-level summaries
    at_event = imp_mat_dense.sum(axis=1)  # total impact per event
    eai_exp = imp_mat_dense.mean(axis=0)  # expected impact per exposure
    aai_agg = eai_exp.sum()

    # Event metadata
    event_id = np.arange(1, len(times) + 1)
    event_name = [f'event_{i}' for i in event_id]
    date = np.array([pd.to_datetime(t).toordinal() for t in times])

    # Frequency from covered years
    start_year = pd.to_datetime(times[0]).year
    end_year = pd.to_datetime(times[-1]).year
    num_years = end_year - start_year + 1
    frequency = np.full(len(times), 1.0 / num_years)

    return Impact(
    event_id=event_id,
    event_name=event_name,
    date=date,
    frequency=frequency,
    frequency_unit=frequency_unit,
    coord_exp=coord_exp,
    crs='',  # optional
    eai_exp=eai_exp,
    at_event=at_event,
    aai_agg=aai_agg,
    unit=unit,
    imp_mat=sparse.csr_matrix(imp_mat_dense),
    haz_type=haz_type
)


def write_impact_to_netcdf(impact, path, var_name="impact", compression=True):
    """
    Save CLIMADA Impact object to a NetCDF file with (time, lat, lon) dimensions.

    Parameters
    ----------
    impact : climada.engine.impact.Impact
        Impact object to save.
    path : str
        Output NetCDF file path.
    var_name : str
        Name of the variable to save.
    compression : bool
        Whether to use compression in the NetCDF.
    """
    # Unpack shapes
    n_time, n_exp = impact.imp_mat.shape

    # Get coordinates
    lat_lon = np.round(impact.coord_exp, 6)
    lats = np.sort(np.unique(lat_lon[:, 0]))
    lons = np.sort(np.unique(lat_lon[:, 1]))

    # Build 2D grid and get mapping index
    lat_grid, lon_grid = np.meshgrid(lats, lons, indexing='ij')
    grid_coords = np.column_stack([lat_grid.ravel(), lon_grid.ravel()])

    # Build mapping from coord_exp to index
    coord_to_index = {tuple(coord): i for i, coord in enumerate(grid_coords)}
    map_index = [coord_to_index.get(tuple(pt), -1) for pt in lat_lon]

    # Check for any unmappable coordinates
    if any(i == -1 for i in map_index):
        raise ValueError("Some coordinates in impact.coord_exp could not be matched to the target grid.")

    # Build full cube and insert values
    cube = np.full((n_time, len(lats), len(lons)), np.nan, dtype=float)
    imp_dense = impact.imp_mat.toarray()
    for exp_i, grid_i in enumerate(map_index):
        lat_i, lon_i = np.unravel_index(grid_i, (len(lats), len(lons)))
        cube[:, lat_i, lon_i] = imp_dense[:, exp_i]

    # Create xarray Dataset
    times = pd.to_datetime([datetime.fromordinal(d) for d in impact.date])
    da = xr.DataArray(cube, coords=[times, lats, lons], dims=["time", "latitude", "longitude"], name=var_name)
    encoding = {var_name: {"zlib": True}} if compression else None

    ds = xr.Dataset({var_name: da})
    ds.to_netcdf(path, encoding=encoding)
    print(f"✅ Impact written to {path}")

    
def get_exposures(haz_type, exposures_dir: Path = EXPOSURES_DIR, age_categories: list = ['all', '0_1', '65_70_75_80'], years: np.ndarray = np.arange(2003, 2023)):
    """
    Load and process exposures data (exposure in the sense of climada, the population) for each age category and year.

    Parameters:
    ----------
    exposures_dir : Path
        The directory containing the exposure HDF5 files.
    age_categories : list, optional
        A list of age categories to process. Default is ['all', '0_1', '65_70_75_80'].
    years : np.ndarray, optional
        An array of years to process. Default is np.arange(2003, 2023).

    Returns:
    -------
    dict
        A dictionary where keys are age categories and each value is another dictionary with years as keys,
        mapping to the corresponding processed Exposures objects.
    """
    exposures_dict = {}

    for age in age_categories:
        exposures_dict[age] = {}
        for year in years:
            year_str = str(year)
            file_path = exposures_dir / f"{age}_era5_025_compatible_{year_str}.hdf5"
            exposure = Exposures.from_hdf5(file_path)

            # Correct longitudes >180 directly in geometry
            exposure.gdf['geometry'] = exposure.gdf.geometry.apply(
                lambda geom: Point(geom.x - 360 if geom.x > 180 else geom.x, geom.y)
            )

            # Set 'impf_<haz_type>' to 1
            exposure.gdf[f"impf_{haz_type}"] = 1 
            
            exposures_dict[age][year_str] = exposure

    return exposures_dict