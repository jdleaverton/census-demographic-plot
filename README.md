# Galveston County Demographic Analysis

This repository contains a Python script for analyzing and visualizing the demographic distribution of Galveston County based on race/ethnicity. The script utilizes geospatial data manipulation and visualization libraries to achieve its objectives.

## Overview

The main Python script, `main.py`, performs the following operations:

1. **Data Loading**: It loads demographic data from a CSV file (`Galveston_county_tract.csv`) and spatial data for Galveston County tracts from a shapefile (`Tracts.shp`).

2. **Data Preparation**: It ensures that the `census_tract_id` column is of the same type in both datasets for merging. Then, it merges the DataFrame containing demographic data with the GeoDataFrame containing spatial data.

3. **Point Generation**: For each race/ethnicity column, it generates random points within the census tracts proportional to the population of that race/ethnicity in the tract.

4. **Data Aggregation**: It combines all generated points into a single GeoDataFrame with a consistent Coordinate Reference System (CRS).

5. **Visualization**: It plots a dot density map showing the distribution of different races/ethnicities across Galveston County. The map includes a basemap for geographical context.

## Libraries Used

- `geopandas`: For working with geospatial data.
- `shapely`: For geometric operations.
- `numpy`: For numerical operations.
- `matplotlib`: For plotting.
- `contextily`: For adding basemaps to plots.
- `pandas`: For data manipulation.
- `logging`: For logging messages.

## How to Run

Ensure you have Python installed along with the required libraries. Run the script using:
```
python main.py
```
