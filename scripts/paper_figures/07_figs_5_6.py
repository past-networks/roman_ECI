import numpy as np
import geopandas as gpd
from shapely import Point

gdf = gpd.read_file("../../data/large_data/LIST_v1-2.geojson")
heatmap = np.log10(gdf["geometry"].map(lambda p: Point(*np.round([p.x, p.y], 2)) if p is not None else None).value_counts() + 1).reset_index()
heatmap = gpd.GeoDataFrame(heatmap, geometry = heatmap["geometry"], crs = "EPSG:3035")
heatmap.to_file("fig_5_latin.shp")

list_dates = gdf[["not_before", "not_after"]].mean(axis = 1).round(-2).sort_values().value_counts(sort = False).reset_index()
list_dates = list_dates[(list_dates["index"] >= -800) & (list_dates["index"] <= 1453)].rename(columns = {"index": "decade"})
list_dates.to_csv("fig_6_latin.csv", index = False, sep = "\t")

gdf = gpd.read_file("../../data/large_data/GIST_v1-1.geojson")
heatmap2 = np.log10(gdf["geometry"].map(lambda p: Point(*np.round([p.x, p.y], 2)) if p is not None else None).value_counts() + 1).reset_index()
heatmap2 = gpd.GeoDataFrame(heatmap, geometry = heatmap["geometry"], crs = "EPSG:3035")
heatmap.to_file("fig_5_greek.shp")

gist_dates = gdf[["not_before", "not_after"]].mean(axis = 1).round(-2).sort_values().value_counts(sort = False).reset_index()
gist_dates = gist_dates[(gist_dates["index"] >= -800) & (gist_dates["index"] <= 1500)].rename(columns = {"index": "decade"})
gist_dates.to_csv("fig_6_greek.csv", index = False, sep = "\t")