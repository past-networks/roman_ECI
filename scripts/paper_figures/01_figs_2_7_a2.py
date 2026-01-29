import rdata, warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category = UserWarning)

dfs = rdata.read_rds("../../results/economic_complexity/province_all_bias_tbs.rds")
df = pd.concat([dfs[x].to_pandas().unstack() for x in dfs if "without_neighbours" in x])
df = df.reset_index()
df.columns = ("occupation", "province", "value")

# All provinces, including language correction
mcp = df.groupby(by = ["province", "occupation"])["value"].mean().reset_index()
mcp = np.log(pd.pivot_table(data = mcp, index = "province", columns = "occupation", values = "value") + 1)
mcp = mcp.loc[mcp.sum(axis = 1).sort_values(ascending = False).index.values, mcp.sum().sort_values(ascending = False).index.values]
row_order_all = mcp.index
col_order_all = mcp.columns
mcp.to_csv("fig_s1_bottom.csv", sep = "\t", index = False, header = False)

# Only Latin provinces, no language correction
dfs = rdata.read_rds("../../results/economic_complexity/filtered_province_all_but_language_bias_tbs.rds")
df = pd.concat([dfs[x].to_pandas().unstack() for x in dfs])
df = df.reset_index()
df.columns = ("occupation", "province", "value")
mcp = df.groupby(by = ["province", "occupation"])["value"].mean().reset_index()
mcp = np.log(pd.pivot_table(data = mcp, index = "province", columns = "occupation", values = "value") + 1)
mcp = mcp.loc[mcp.sum(axis = 1).sort_values(ascending = False).index.values, mcp.sum().sort_values(ascending = False).index.values]
row_order = mcp.index
col_order = mcp.columns
max_value = mcp.max().max()
mcp.to_csv("fig_1_b.csv", sep = "\t", index = False, header = False)

provinces = set(mcp.index)

df = pd.read_csv("../../results/economic_complexity/province_table.csv", index_col = 0)

# All provinces, no corrections
mcp = np.log(df + 1)
mcp = mcp.reindex(index = row_order_all, columns = col_order_all).fillna(0.0)
mcp.to_csv("fig_s1_top.csv", sep = "\t", index = False, header = False)

# Only Latin provinces, no corrections
df = df[df.index.isin(provinces)]
mcp = np.log(df + 1)
mcp = mcp.reindex(index = row_order, columns = col_order).fillna(0.0)
min_value = (mcp[mcp > 0]).min().min()
mcp.to_csv("fig_1_a.csv", sep = "\t", index = False, header = False)
