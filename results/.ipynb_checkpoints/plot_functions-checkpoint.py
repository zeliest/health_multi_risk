from cartopy import crs
import matplotlib as mpl
import copy
import datetime
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon, box
from climada.util.multi_risk import combine_impacts

from climada.util.multi_risk import *
from cartopy import crs
import matplotlib as mpl
import copy
import datetime
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, MultiPolygon, box
from climada.util.multi_risk import combine_impacts

def calculate_risk_score(imp_combined, agg_regions, gdf_adm1, age, hazards, risk_score_type):
    """
    Calculate and visualize the risk score for a specified age group and number of hazards.

    This function processes impact data based on the age group and the number of hazards. It calculates either 
    the absolute impact or the relative impact (per population) and generates a world map visualizing the risk 
    scores at the regional level.

    Parameters:
    -----------
    imp_combined : dict with impact combination
    age : str
        Age group to consider (e.g., 'all', '0_1', '65_70_75_80').
    hazards : int
        Number of hazards to consider (1, 2, or 3).
    risk_score_type : str
        Type of risk score to calculate ('impact' for absolute impact, 'relative_impact' for relative impact per population).

    Returns:
    --------
    gdf_merged : GeoDataFrame
        A GeoDataFrame containing the merged data with calculated risk scores, ready for geographical visualization.

    Raises:
    -------
    ValueError:
        If the number of hazards is not 1, 2, or 3.

    Example:
    --------
    result = calculate_risk_score('all', 3, 'impact')
    """
    
    # Validate the number of hazards
    if hazards not in [1, 2, 3]:
        raise ValueError("Hazards must be 1, 2, or 3.")
    
    # Identify the appropriate keys based on the number of hazards
    if hazards == 3:
        tuple_keys = [key for key in imp_combined[age].keys() if len(key.replace("RF_2y","RF")) == 8]
    elif hazards == 2:
        tuple_keys = [key for key in imp_combined[age].keys() if len(key.replace("RF_2y","RF")) == 5]
    else:
        tuple_keys = [key for key in imp_combined[age].keys() if len(key.replace("RF_2y","RF")) == 2]
    
    # Filter the impacts based on the number of hazards
    imp_combined_hazards = {
        key: imp_combined[age][key]
        for key in tuple_keys
        if imp_combined[age][key].imp_mat.nnz > 0
    }
    
    # Combine impacts using "max" method for at least the specified number of hazards
    combined_impacts = combine_impacts(imp_combined_hazards, how="max")
    
    # Aggregate impacts at the regional level
    imp_combined_at_reg = combined_impacts.impact_at_reg(agg_regions=agg_regions['numeric'])
    
    # Prepare the data for plotting
    at_reg = copy.deepcopy(imp_combined_at_reg)
    at_reg['month'] = [datetime.datetime.fromordinal(int(date)).month for date in imp_combined[age][tuple_keys[0]].date]
    at_reg['year'] = [datetime.datetime.fromordinal(int(date)).year for date in imp_combined[age][tuple_keys[0]].date]
    
    # Melt and merge data
    at_reg_melted = at_reg.melt(id_vars=['month', 'year'], var_name='numeric', value_name='impact')
    at_reg_melted = at_reg_melted.merge(agg_regions[["ADM1_ID", "ADM1_NAME", "ISO3", "numeric"]].drop_duplicates())
    at_reg_melted = at_reg_melted.merge(adm1_pop_by_year, on=['year', "ADM1_ID", "ADM1_NAME", "ISO3"], how='inner')
    
    # Calculate relative impact if needed
    if risk_score_type == 'relative_impact':
        at_reg_melted['relative_impact'] = at_reg_melted['impact'] / at_reg_melted['value']
        at_reg_melted['Risk Score'] = at_reg_melted['relative_impact']
    else:
        at_reg_melted['Risk Score'] = at_reg_melted['impact']
    
    # Calculate the mean impact across months for each region
    mean_imp_at_reg = at_reg_melted.groupby(["ADM1_ID", "ADM1_NAME", "ISO3"]).mean().reset_index()
    
    # Prepare the geographical data
    robinson = crs.Robinson().proj4_init
    gdf_merged = gdf_adm1.merge(mean_imp_at_reg, on=["ADM1_ID", "ADM1_NAME", "ISO3"], how='right')
    gdf_merged["geometry"] = gdf_merged["geometry"].clip((-180, -59.48, 179.9999999, 83.64))
    gdf_merged = gdf_merged.to_crs(robinson)
    
    # Plotting the risk score map
    fig = plt.figure(figsize=(8, 6))
    vmin = gdf_merged['Risk Score'].min()
    vmax = gdf_merged['Risk Score'].max()
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    
    # ax = fig.add_subplot(1, 1, 1)
    # gdf_merged.plot(column='Risk Score', cmap=cmaps[age], ax=ax, vmax=vmax)
    # plt.axis('off')
    
    # cbar = plt.cm.ScalarMappable(cmap=cmaps[age], norm=norm)
    # ax_cbar = fig.colorbar(cbar, ax=ax, orientation='horizontal')
    # ax_cbar.set_label(f'Risk Score')
    # ax_cbar.set_ticks([])
    
    # Save the processed data
    at_reg_melted.to_csv(DATA_DIR / f"impacts/three_or_more_{age}.csv")

    return gdf_merged

# Example usage:
# result = calculate_risk_score('all', 3, 'impact')
