Note: This code makes use of CLIMADA v6.0.1. and dependencies.
For installation instructions, see the official documentation:
https://climada-python.readthedocs.io/en/stable/guide/install.html

# Folders Description

## prepare_hazard_data
In this folder, we preprocess the data for the different hazards. 

## prepare_population_data
In this folder, we preprocess the data for the population

## exposure_to_hazard
Here we overlay the population and hazards data, and then we combine the different hazards to assess exposure to multi-hazards. The default is to read CLIMADA Impact objects, but also netcdf can be read as impacts to then compute the combinations and plot the results.

## results
We here generate the main plots, generating hotspots, ...

