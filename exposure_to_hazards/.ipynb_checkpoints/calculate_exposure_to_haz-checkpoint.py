from pathlib import Path
from climada.entity import Exposures
from climada.engine import Impact
import numpy as np
import sys
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
            exposure.gdf['longitude'] = exposure.gdf['longitude'].where(exposure.gdf['longitude'] <= 180, exposure.gdf['longitude'] - 360)
            # Set 'impf_DR' to 1
            exposure.gdf[f"impf_{haz_type}"] = 1 
            
            exposures_dict[age][year_str] = exposure

    return exposures_dict