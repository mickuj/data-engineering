#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import json
import geopandas as gpd

with open('proj4_params.json') as f:
    params = json.load(f)
id_column = params['id_column']

points = gpd.read_file('proj4_points.geojson')
points.plot()
points


# In[19]:


points_proj = points.to_crs(epsg=2180)
area = points_proj.copy()
area['geometry'] = area.buffer(100)
joined = gpd.sjoin(area, points_proj, predicate='intersects')
counts = (joined.groupby(id_column + '_left').size().reset_index(name='count').rename(columns={id_column + '_left': id_column}))

counts.to_csv('proj4_ex01_counts.csv', index=False)
counts


# In[3]:


points_latlon = points.to_crs(epsg=4326)
points_latlon['lat'] = points_latlon.geometry.y.round(7)
points_latlon['lon'] = points_latlon.geometry.x.round(7)

points_latlon[[id_column, 'lat', 'lon']].to_csv('proj4_ex01_coords.csv', index=False)


# In[27]:


from pyrosm import OSM, get_data
from shapely.ops import linemerge

osm = OSM(get_data('Cracow'))
roads = osm.get_network('driving')
roads = roads[roads['highway'] == 'tertiary']
roads["geometry"] = roads["geometry"].apply(lambda x: linemerge(x) if x.geom_type == "MultiLineString" else x)
roads = roads[['id', 'name', 'geometry']]
roads.columns = ['osm_id', 'name', 'geometry']

roads.to_file('proj4_ex02_roads.geojson', driver='GeoJSON')
roads


# In[29]:


roads = gpd.read_file('proj4_ex02_roads.geojson')
points = gpd.read_file('proj4_points.geojson')

roads_proj = roads.to_crs(epsg=2180)
points_proj = points.to_crs(epsg=2180)

roads_buff = roads_proj.copy()
roads_buff['geometry'] = roads_proj.geometry.buffer(50, cap_style=2)

joined = gpd.sjoin(roads_buff, points_proj, predicate='intersects')
joined = joined.drop_duplicates(subset='lamp_id')

counts = (joined.groupby('name').size().reset_index(name='point_count'))
counts = counts[counts['name'].notnull()]

counts.to_csv('proj4_ex03_streets_points.csv', index=False)
counts


# In[18]:


import matplotlib.pyplot as plt
import contextily as ctx

countries = gpd.read_file('proj4_countries.geojson')
countries.to_pickle('proj4_ex04_gdf.pkl')
countries_proj = countries.to_crs(epsg=3857)

for idx, row in countries_proj.iterrows():
    country_name = row['name'].lower().replace(' ', '_')
    geometry = row['geometry']
    fig, ax = plt.subplots(figsize=(8, 8))

    gdf_single = gpd.GeoDataFrame([row], crs=countries_proj.crs)
    gdf_single.boundary.plot(ax=ax, edgecolor='blue', linewidth=2)
    ctx.add_basemap(ax, crs=countries_proj.crs)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.savefig(f'proj4_ex04_{country_name}.png', bbox_inches='tight', dpi=300)
    plt.close()

