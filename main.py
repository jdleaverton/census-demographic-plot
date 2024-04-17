import geopandas as gpd  # Importing the geopandas library for working with geospatial data
from shapely.geometry import Point
from shapely.geometry import MultiPoint  # Importing MultiPoint for creating collections of points
from shapely.ops import unary_union  # Importing unary_union for merging geometries
import numpy as np  # Importing numpy for numerical operations
import matplotlib.pyplot as plt  # Importing matplotlib for plotting
import contextily as ctx  # Importing contextily for adding basemaps to plots
import pandas as pd  # Importing pandas for data manipulation
import logging  # Importing logging to log messages
import random # Importing random to generate random numbers
import datetime # Importing datetime to generate a timestamp

# Setting up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('Galveston_county_tract.csv')
logging.info('CSV file loaded successfully.')

# Load the spatial dataset for Galveston County tracts
tracts_shapefile = 'Tracts.shp'
galveston_tracts_geo = gpd.read_file(tracts_shapefile)
logging.info('Spatial dataset loaded successfully.')
logging.info(f"Columns in galveston_tracts_geo: {galveston_tracts_geo.columns.tolist()}")

# Ensure the 'census_tract_id' column is of the same type in both datasets for merging
df['census_tract_id'] = df['census_tract_id'].astype(str)
galveston_tracts_geo['census_tract_id'] = galveston_tracts_geo['TRT'].astype(str)

# Merge the DataFrame with the GeoDataFrame on 'census_tract_id'
galveston_tracts = galveston_tracts_geo.merge(df, on='census_tract_id')

# List all columns in the GeoDataFrame
print("All columns:", galveston_tracts.columns.tolist())

# Identify geometry columns
geometry_columns = galveston_tracts.dtypes[galveston_tracts.dtypes == 'geometry'].index.tolist()
print("Geometry columns:", geometry_columns)

# Check the active geometry column
print("Active geometry column:", galveston_tracts.geometry.name)

galveston_tracts = galveston_tracts.set_geometry('geometry')
logging.info('DataFrames merged successfully.')

def generate_random_points(poly, num_points):
    points = []
    minx, miny, maxx, maxy = poly.bounds
    while len(points) < num_points:
        pnt = Point(random.uniform(minx, maxx), random.uniform(miny, maxy))
        if poly.contains(pnt):
            points.append(pnt)
    return MultiPoint(points)
    
# Function to apply generate_points to each row of the DataFrame
def apply_generate_points(row, column_name):
    num_points = int(row[column_name])  # Convert to integer if not already
    return generate_random_points(row['geometry'], num_points)

# Generate points for different races using the correct column names
race_columns = ['race_hispanic', 'race_white', 'race_black', 'race_asian']
for race in race_columns:
    galveston_tracts[f"{race}_points"] = galveston_tracts.apply(apply_generate_points, column_name=race, axis=1)
logging.info('Points generated for each race.')

# Combine all points into a single GeoDataFrame with consistent CRS
all_points_list = []
for race in race_columns:
    # Extract the points column and rename it to 'geometry'
    geometry_data = galveston_tracts[f"{race}_points"].copy()
    geometry_data.name = "geometry"
    
    # Create a GeoSeries from the geometry data
    geometry_series = gpd.GeoSeries(geometry_data, crs=galveston_tracts.crs)
    
    # Create a temporary DataFrame with the 'race' column
    temp_df_data = pd.DataFrame({'race': [race.split('_')[1].capitalize()] * len(galveston_tracts)})
    
    # Combine the GeoSeries and the temporary DataFrame into a GeoDataFrame
    temp_df = gpd.GeoDataFrame(temp_df_data, geometry=geometry_series, crs=galveston_tracts.crs)
    
    # Append the temporary GeoDataFrame to the list
    all_points_list.append(temp_df)

# Now, combine the GeoDataFrames from the list into a single GeoDataFrame
all_points = gpd.GeoDataFrame(pd.concat(all_points_list, ignore_index=True), crs=galveston_tracts.crs)
logging.info('All points combined into a single GeoDataFrame with consistent CRS.')

# Plotting
fig, ax = plt.subplots(figsize=(10, 10))
galveston_tracts.plot(ax=ax, edgecolor='black', facecolor='none')
all_points.plot(ax=ax, column='race', legend=True, alpha=0.6, markersize=8)

# Add a basemap
ctx.add_basemap(ax, crs=galveston_tracts.crs.to_string(), source=ctx.providers.OpenStreetMap.Mapnik)
ax.set_title('Dot Density Map of Race/Ethnicity in Galveston County')
plt.show()
logging.info('Plot generated successfully.')

# Generate a timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Save the plot in the 'output' folder with the timestamp
plt.savefig(f'output/dot_density_map_{timestamp}.png')
logging.info(f'Plot saved as dot_density_map_{timestamp}.png in the output folder.')


# Initialize a list to hold the summary data
summary_data = []

# Iterate over each row in the galveston_tracts GeoDataFrame
for index, row in galveston_tracts.iterrows():
    # Extract the census tract ID
    census_tract_id = row['census_tract_id']
    
    # Count the number of points for each race
    # Use .geoms on each MultiPoint object to get an iterable of Point objects, then use len() to count them
    hispanic_points_count = len(row['race_hispanic_points'].geoms) if row['race_hispanic_points'] else 0
    white_points_count = len(row['race_white_points'].geoms) if row['race_white_points'] else 0
    black_points_count = len(row['race_black_points'].geoms) if row['race_black_points'] else 0
    asian_points_count = len(row['race_asian_points'].geoms) if row['race_asian_points'] else 0
    
    # Append the counts to the summary data list
    summary_data.append({
        'Census Tract ID': census_tract_id,
        'Hispanic': hispanic_points_count,
        'White': white_points_count,
        'Black': black_points_count,
        'Asian': asian_points_count
    })

# Convert the summary data into a DataFrame
summary_df = pd.DataFrame(summary_data)

# Print the DataFrame in a well-formatted table
print(summary_df.to_string(index=False))