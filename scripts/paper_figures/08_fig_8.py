import pandas as pd

ecis = pd.read_csv("../../results/economic_complexity/filtered_province_all_but_language_bias_eci_df.csv", index_col = 0).set_index("province")[["eci",]]

ecis.index = ecis.index.map(lambda x: x if len(x) <= 16 else f"{x[:13]}...")

ecis = ecis.groupby(by = "province").quantile(q = [0.1, 0.25, 0.5, 0.75, 0.9]).reset_index()
pd.pivot_table(data = ecis, index = "province", columns = "level_1", values = "eci").reset_index().sort_values(by = 0.50, ascending = False).to_csv("fig_8.csv", sep = "\t", index = False, header = False)