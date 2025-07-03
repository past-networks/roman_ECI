import pandas as pd
import geopandas as gpd

eci_bias = pd.read_csv("../../results/economic_complexity/province_table.csv", sep = "\t").rename(columns = {"eci": "eci_biased"})
ecis = pd.read_csv("../../results/economic_complexity/filtered_province_all_but_language_bias_eci_df.csv", index_col = 0).groupby(by = "province")["eci"].mean().reset_index().rename(columns = {"eci": "eci_avg"})

provinces = set(ecis["province"])

gdf = gpd.read_file("../../data/economic_complexity/provinces/provinces.shp")
gdf = gdf.merge(ecis, on = "province", how = "left")
gdf = gdf.merge(eci_bias[eci_bias["province"].isin(provinces)], on = "province", how = "left")
gdf = gdf.fillna(-2)
gdf.to_file("figs_4_7.shp")

ecis = pd.read_csv("../../results/economic_complexity/province_all_bias_eci_df.csv", index_col = 0)
ecis = ecis[ecis["m"] == "r_0"].groupby(by = "province")["eci"].mean().reset_index().rename(columns = {"eci": "eci_avg"})

gdf = gpd.read_file("../../data/economic_complexity/provinces/provinces.shp")
gdf = gdf.merge(ecis, on = "province", how = "left")
gdf = gdf.merge(eci_bias, on = "province", how = "left")
gdf = gdf.fillna(-2)
gdf.to_file("fig_s3.shp")