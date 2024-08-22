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


colors_dict_combi = {
    'RF': '#1f77b4',  # Blue
    'EP': '#1c4e80',  # Dark Blue
    'DR': '#a8a8a8',  # Grey
    'HW': 'red',  # Red
    'FI': '#ff5733',  # Orange
    'TC': '#17becf',  # Teal

    # Combinations
    'RF-EP': 'yellow',  # Mixed Blue
    'RF-DR': '#7497b4',  # Light Blue Grey
    'RF-HW': '#b46649',  # Reddish Blue
    'RF-FI': '#9c6776',  # Muted Red-Blue
    'RF-TC': '#1ca9b4',  # Light Teal

    'EP-DR': '#58749d',  # Dark Blue-Grey
    'EP-HW': '#745569',  # Dark Red-Blue
    'EP-FI': '#823344',  # Dark Reddish Blue
    'EP-TC': 'green',  # Dark Teal

    'DR-HW': 'pink',  # Warm Grey
    'DR-FI': '#c49a76',  # Greyish Orange
    'DR-TC': '#9db4c3',  # Greyish Teal

    'HW-FI': 'maroon',  # 
    'HW-TC': '#ff9266',  # Orange Teal

    'FI-TC': '#ff8466',  # Orange Teal mix

    # Triple combinations
    'RF-EP-DR': '#64768a',  # Muted Blue Grey
    'RF-EP-HW': '#8a7373',  # Muted Red Blue
    'RF-EP-FI': '#8b6473',  # Muted Orange Blue
    'RF-EP-TC': '#5293a4',  # Muted Teal Blue

    'RF-DR-HW': '#a8806b',  # Warm Greyish Blue
    'RF-DR-FI': 'darkgreen',  # Warm Greyish Red
    'RF-DR-TC': '#85a1b6',  # Light Greyish Teal
    'RF-EP-TC':'yellow',
    'RF-HW-FI': '#d4806d',  # Warm Red Orange
    'RF-HW-TC': '#c7807e',  # Warm Red Teal
    'RF-FI-TC': '#c07b71',  # Warm Orange Teal

    'EP-DR-HW': 'green',  # Grey Blue Red
    'EP-DR-FI': '#84697b',  # Grey Blue Orange
    'EP-DR-TC': '#7290a3',  # Grey Blue Teal

    'EP-HW-FI': '#99656d',  # Red Blue Orange
    'EP-HW-TC': 'purple',  # Red Blue Teal
    'EP-FI-TC': '#a36c7b',  # Orange Blue Teal

    'DR-HW-FI': 'magenta',  # Warm Grey Orange
    'DR-HW-TC': '#b29a85',  # Warm Grey Teal
    'DR-FI-TC': '#bb9a80',  # Grey Orange Teal

    'HW-FI-TC': '#ff9980',  # Bright Orange Teal

    # Quadruple combinations
    'RF-EP-DR-HW': '#9d857a',  # Muted Warm Grey
    'RF-EP-DR-FI': '#95787a',  # Muted Warm Red
    'RF-EP-DR-TC': '#7d9ba6',  # Muted Warm Teal
    'RF-EP-HW-FI': '#a4817a',  # Warm Red Orange
    'RF-EP-HW-TC': '#91807d',  # Muted Warm Teal
    'RF-EP-FI-TC': '#987b7d',  # Warm Orange Teal
    'RF-DR-HW-FI': '#b67a72',  # Greyish Warm Red
    'RF-DR-HW-TC': '#9e857e',  # Greyish Warm Teal
    'RF-DR-FI-TC': '#a37d78',  # Greyish Orange Teal
    'RF-HW-FI-TC': '#bf8a7b',  # Warm Reddish Orange Teal
    'EP-DR-HW-FI': '#a47a7d',  # Dark Warm Grey
    'EP-DR-HW-TC': '#8a818c',  # Dark Greyish Teal
    'EP-DR-FI-TC': '#987a83',  # Dark Greyish Orange Teal
    'EP-HW-FI-TC': '#9f7b81',  # Dark Reddish Orange Teal
    'DR-HW-FI-TC': '#c79b82',  # Warm Greyish Orange Teal
}


def calculate_risk_score(imp_combined, agg_regions, gdf_adm1, adm1_pop_by_year, age, hazards, risk_score_type):
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
    imp_combined_subset = {
        key: imp_combined[age][key]
        for key in tuple_keys
        if imp_combined[age][key].imp_mat.nnz > 0
    }
    
    # Combine impacts using "max" method for at least the specified number of hazards
    imp_combined_all = combine_impacts(imp_combined_subset, how="max")
    
    # Aggregate impacts at the regional level
    at_reg = imp_combined_all.impact_at_reg(agg_regions=agg_regions['numeric'])
    
    # Prepare the data for plotting
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


    return at_reg_melted




def impact_select_region(impact, region_coord, region_num):
    """
    Create a new impact object containing only the data for a specified country.

    This function filters an existing impact object to include only the data points
    that are within the boundaries of a given country. The function uses latitude and 
    longitude coordinates from the 'impact' object to determine the country of each 
    data point. It then filters the impact matrix and coordinates to include only those
    corresponding to the specified country.

    The country is specified by its ISO3 3166-1 numeric code as a three-digit string. 
    For example, '840' for the United States, '124' for Canada, and '392' for Japan.

    Parameters:
    ----------
    impact : Impact
        The impact object to be filtered. This object should contain latitude and 
        longitude coordinates ('coord_exp') and an impact matrix ('imp_mat').

    country : str
        The three-digit string representing the ISO3 3166-1 numeric country code.

    Returns:
    -------
    Impact
        A new Impact object containing only the data for the specified country.
    """
    lat, lon = np.array(impact.coord_exp).T
    imp_mat = impact.imp_mat[:, region_coord == np.array(region_num)[0]]
    coord_exp = impact.coord_exp[region_coord == np.array(region_num)[0]]
    at_event, eai_exp, aai_agg = ImpactCalc.risk_metrics(imp_mat, impact.frequency)
    
    impact_region = Impact(
        event_id=impact.event_id,
        event_name=impact.event_name,
        date=impact.date,
        at_event=at_event,
        eai_exp=eai_exp,
        aai_agg=aai_agg,
        coord_exp=coord_exp,
        crs=DEF_CRS,
        imp_mat=imp_mat,
        frequency=impact.frequency,
        unit=impact.unit,
        frequency_unit=impact.unit,
    )
    return impact_region
