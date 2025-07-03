import glob
import numpy as np
import pandas as pd
from scipy.linalg import eig
from scipy.stats import spearmanr

def load_data(input_file):
   rome = pd.read_csv(f"../../results/economic_complexity/{input_file}.csv", index_col = 0)[["country", "eci"]]
   rome = rome.groupby(by = "country").mean().reset_index()
   df = rome.merge(modern, left_on = "country", right_on = "exporter", suffixes = ("_rome", "_modern"), how = "left").drop("exporter", axis = 1)
   df["eci_rome_rank"] = df["eci_rome"].rank(ascending = False)
   df["eci_modern_rank"] = df["eci_modern"].rank(ascending = False)
   return df

# NOTE: The trade data is large (6.5GB) and is not included in out Github
# Please populate the ../../data/modern_trade/ folder with the data from https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/H8SFD2&version=10.0
# Specifically all sitc_country_country_product_year_4_*_*.dta files
# In addition, the location_country and product_sitc files from https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/3BAL1O&version=6.0  
ccpy = pd.concat([pd.read_stata(dta) for dta in glob.glob("../../data/modern_trade/*.dta")])
countries = pd.read_csv("../../data/modern_trade/location_country.tab", sep = "\t")
sitc = pd.read_csv("../../data/modern_trade/product_sitc.tab", sep = "\t")
# The whitelist is the list of countries within the span of the Roman Empire
whitelist = set(pd.read_csv("country_whitelist.csv", sep = "\t")["country"])

ccpy = ccpy[ccpy["export_value"] > 0]
ccpy = ccpy.drop(["import_value", "coi", "eci", "pci"], axis = 1).merge(countries[["country_id", "iso3_code"]], on = "country_id")
ccpy = ccpy.drop("country_id", axis = 1).rename(columns = {"iso3_code": "exporter"})
ccpy = ccpy.merge(countries[["country_id", "iso3_code"]], left_on = "partner_country_id", right_on = "country_id")
ccpy = ccpy.drop(["partner_country_id", "country_id"], axis = 1).rename(columns = {"iso3_code": "importer"})

blacklist = set([
   # 1) The only measurement we have is geographical distance
   "ANT", "PAL", "REU", "STP", "TKL", "TMP", "YUG",
   # 2) Zero or very low (< 300M) GDP, with the exception of: Kosovo, Myanmar, North Korea, Somalia
   "ALA", "ASM", "AIA", "ATA", "BES", "BVT", "IOT", "VGB", "CXR", "CCK", "COK", "CUW", "FLK", "FRO", "GUF", "PYF", "ATF", "GRL", "GLP", "GUM", "GGY", "HMD", "VAT", "IMN", "JEY", "KIR", "LIE", "MHL", "MYT", "MSR", "NRU", "NCL", "NIU", "NFK", "MNP", "PLW", "PCN", "REU", "BLM", "SHN", "MAF", "SPM", "STP", "SXM", "SGS", "SJM", "TKL", "TCA", "TUV", "UMI", "VIR", "WLF", "ESH",
   # 3) Countries with less than 300k inhabitans
   "BRB", "VUT", "WSM", "LCA", "VCT", "GRD", "TON", "FSM", "SYC", "ATG", "AND", "DMA", "BMU", "CYM", "KNA", "MCO", "SMR", "GIB", "ABW",
   # 4) For some reason, Ethiopia is not working
   "ETH",
   # 5) Codes not referring to countries
   "QZZ", "WLD", "ANS", "USP", "PCZ"
   # 6) Countries with no distance information
   "COD", "MAC", "SSD", "TLS"
])

exporters = ccpy.groupby(by = "exporter")["export_value"].sum().reset_index()
exporters = exporters.sort_values(by = "export_value")
exporters["share"] = exporters["export_value"].cumsum()
exporters["share"] /= exporters["share"].max()
blacklist |= set(exporters.loc[exporters["share"] <= 0.0001, "exporter"])

importers = ccpy.groupby(by = "importer")["export_value"].sum().reset_index()
importers = importers.sort_values(by = "export_value")
importers["share"] = importers["export_value"].cumsum()
importers["share"] /= importers["share"].max()
blacklist |= set(importers.loc[importers["share"] <= 0.0005, "importer"])

blacklist -= whitelist

products = ccpy.groupby(by = "product_id")["export_value"].sum().reset_index()
products = products.sort_values(by = "export_value")
products["share"] = products["export_value"].cumsum()
products["share"] /= products["share"].max()
products = products[products["share"] > 0.025]

ccpy = ccpy[~ccpy["importer"].isin(blacklist)]
ccpy = ccpy[~ccpy["exporter"].isin(blacklist)]
ccpy = ccpy[ccpy["product_id"].isin(set(products["product_id"]))]

ccpy = ccpy.merge(sitc[["product_id", "code"]], on = "product_id").drop("product_id", axis = 1).rename(columns = {"code": "sitc"})

mcp = ccpy.groupby(by = ["exporter", "sitc"])["export_value"].sum().reset_index()
mcp = pd.pivot_table(data = mcp, index = "exporter", columns = "sitc", values = "export_value").fillna(0.0)

mcp = ((mcp / mcp.sum()).T / (mcp.sum(axis = 1) / mcp.sum().sum())).T > 1
ubiquity = mcp.sum(axis = 0) # Sums the number of exporters exporting the product with RCA > 1
diversity = mcp.sum(axis = 1) # Sums the number of products exported by the exporter with RCA > 1

Q = mcp / ubiquity # Column normalized M_cp
R = (mcp.T / diversity).T # Row normalized M_cp
Scc = np.dot(Q, R.T).astype(float) # Square exporter-exporter matrix

Scc_eigen = eig(Scc, left = True)
idx = Scc_eigen[0].argsort()  # Numpy returns eigenvectors in random order, so we need to sort them so that we are sure we're picking the second largest
eci = np.real(Scc_eigen[1][:,idx][:,-2])

if np.corrcoef(eci, diversity)[0,1] < 0:
   eci *= -1

modern = mcp.reset_index().merge(pd.DataFrame(eci), left_index = True, right_index = True)[["exporter", 0]].rename(columns = {0: "eci"})

df_latin = load_data("filtered_country_all_but_language_bias_eci_df")
df_all = load_data("country_all_bias_eci_df")

print(spearmanr(df_latin["eci_rome"], df_latin["eci_modern"]))
print(spearmanr(df_all["eci_rome"], df_all["eci_modern"]))

df_latin.to_csv("tab_1.csv", sep = "\t", index = False)
