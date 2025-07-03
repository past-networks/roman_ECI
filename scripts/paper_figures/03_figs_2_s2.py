import rdata, warnings
import numpy as np
import pandas as pd
import networkx as nx
import backboning as bb

warnings.filterwarnings("ignore", category = UserWarning)

def reconnect_singletons(df, df_bb, nodes):
   additional_edges = []
   missing_nodes = nodes - (set(df_bb["src"]) | set(df_bb["trg"]))
   for missing_node in missing_nodes:
      try:
         missing_node_edges = df[(df["src"] == missing_node) | (df["trg"] == missing_node)]
         additional_edges.append(pd.DataFrame(missing_node_edges.loc[missing_node_edges["score"].idxmax()]).T)
      except ValueError:
         pass
   additional_edges = pd.concat(additional_edges).drop_duplicates()
   print(additional_edges.shape[0], 1 - additional_edges["score"].mean())
   return pd.concat([df_bb, additional_edges])

def reconnect_components(df, df_bb):
   G = nx.from_pandas_edgelist(df_bb, source = "src", target = "trg")
   ccs = list(nx.connected_components(G))
   ccs = {n: i for i in range(len(ccs)) for n in ccs[i]}
   df["src_comp"] = df["src"].map(ccs)
   df["trg_comp"] = df["trg"].map(ccs)
   additional_edges = []
   while df[["src_comp", "trg_comp"]].value_counts().size > 1:
      new_edge = df.loc[df.loc[df["src_comp"] != df["trg_comp"], "score"].idxmax()]
      new_edge_df = pd.DataFrame(new_edge[["src", "trg", "nij", "score"]]).T
      df_bb = pd.concat([df_bb, new_edge_df])
      additional_edges.append(new_edge_df)
      new_comp = new_edge[["src_comp", "trg_comp"]].min().min()
      old_comp = new_edge[["src_comp", "trg_comp"]].max().max()
      df.loc[df["src_comp"] == old_comp, "src_comp"] = new_comp
      df.loc[df["trg_comp"] == old_comp, "trg_comp"] = new_comp
   additional_edges = pd.concat(additional_edges).drop_duplicates()
   print(additional_edges.shape[0], 1 - additional_edges["score"].mean())
   return df_bb

def build_os(datafile, tag):
   dfs = rdata.read_rds(f"../../results/economic_complexity/{datafile}.rds")
   df = pd.concat([dfs[x].to_pandas().unstack() for x in dfs if tag == "" or "without_neighbours" in x])
   df = df.reset_index()
   df.columns = ("occupation", "province", "value")
   mcp = df.groupby(by = ["province", "occupation"])["value"].mean().reset_index()
   mcp = np.log(pd.pivot_table(data = mcp, index = "province", columns = "occupation", values = "value") + 1)
   df = mcp.T.dot(mcp).unstack()
   df.index.names = ("src", "trg")
   df = df.reset_index().rename(columns = {0: "nij"})
   df = df[(df["src"] != df["trg"]) & (df["nij"] > 0)]
   df_nc = bb.noise_corrected(df, undirected = True)
   df_nc_bb = bb.thresholding(df_nc, 20.5)
   df_nc_bb = reconnect_singletons(df_nc, df_nc_bb, set(mcp.columns))
   df_nc_bb = reconnect_components(df_nc, df_nc_bb)
   df_nc_bb.to_csv(f"fig_{tag}2_edges.csv", index = False, sep = "\t")
   df_nodes = mcp.T
   df_nodes["tot"] = df_nodes.sum(axis = 1)
   df_nodes.reset_index().to_csv(f"fig_{tag}2_nodes.csv", index = False, sep = "\t")

build_os("filtered_province_all_but_language_bias_tbs", "")
build_os("province_all_bias_tbs", "s")