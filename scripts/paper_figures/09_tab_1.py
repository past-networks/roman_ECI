import rdata, warnings
import pandas as pd

warnings.filterwarnings("ignore", category = UserWarning)

dfs = rdata.read_rds("../../results/economic_complexity/filtered_province_all_but_language_bias_tbs.rds")
df = pd.concat([dfs[x].to_pandas().unstack() for x in dfs])
df = df.reset_index()
df.columns = ("occupation", "province", "value")
mcp = df.groupby(by = ["province", "occupation"])["value"].mean().reset_index()

ecis = pd.read_csv("../../results/economic_complexity/filtered_province_all_but_language_bias_eci_df.csv", index_col = 0).groupby(by = "province")["eci"].mean().reset_index().rename(columns = {"eci": "eci_avg"})

provinces = set(mcp["province"])

df = pd.read_csv("../../results/economic_complexity/biased_table.csv", index_col = 0)

df = df[df.index.isin(provinces)]

table = pd.DataFrame()
table["inscription_count"] = df.sum(axis = 1)
table["occupation_diversity"] = (df > 0).sum(axis = 1)
table["adjusted_occupation_numbers"] = mcp.groupby(by = "province")["value"].sum()
table["eci"] = ecis.set_index("province")["eci_avg"]

table = table.sort_values(by = "inscription_count", ascending = False)
table["adjusted_occupation_numbers"] = table["adjusted_occupation_numbers"].round().astype(int).map('{:,}'.format)
table["inscription_count"] = table["inscription_count"].astype(int).map('{:,}'.format)

print(table.to_latex(float_format = "{:.2f}".format))
