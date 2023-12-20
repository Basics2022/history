
import os, glob
import pandas as pd
import geopandas as gpd
import json

#> -----------------------------------------------------------------------------
#> Data input
#>> Political divisions (.geojson, or .shp?)
# folder, filen_root, filen_ext = './../../geojson/', 'world_', '.geojson'
folder, filen_root, filen_ext = './../../../maps/qgis/', 'world_', '.shp'
min_year, max_year = 1700, 2023
pol_year_exceptions = [1930, 1960]

#>> Colormap file
colormap_file = './colors_politics.json'

if ( os.path.isfile(colormap_file) ):

    with open(colormap_file, 'r') as f:
        color_dict = dict(json.load(f))

else:
    color_dict = {}

print(f"color_dict: \n{color_dict}")

#> -----------------------------------------------------------------------------
#> Load map files and update color_dict
#>> Political divisions
file_ls = glob.glob(folder+filen_root+'*'+filen_ext) # file list
year_list = []                                       # list of years (str)
for f in file_ls:
    if ( not f in pol_year_exceptions ):
        year = int(f.replace(folder+filen_root,'').replace(filen_ext,'').replace('bc','-'))
        if ( min_year <= year and year <= max_year ):
            year_list += [ str(year) ]
year_list = sorted(year_list, key=int)
print(f"year_list: {year_list}")

pol_filen_list = [ folder+filen_root+str(y).replace("-","bc")+filen_ext for y in year_list]

pol_list =  [ gpd.read_file(f) for f in pol_filen_list ]

#> -----------------------------------------------------------------------------
default_color = 'rgb(128,128,128)'
for f in pol_filen_list:
    gdf = gpd.read_file(f)
    print(f"{f}:\n{gdf.head()}")
    for index, row in gdf.iterrows():
        color_dict[row['NAME']] = color_dict.get(row['NAME'], default_color)
        if row['NAME'] == None:
            print(index)

color_dict = dict(sorted(color_dict.items()))
print(f"color_dict: \n{color_dict}")

# Convert and write JSON object to file
with open(colormap_file, "w") as outfile: 
    json.dump(color_dict, outfile, indent=4)

