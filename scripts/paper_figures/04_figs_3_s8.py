import numpy as np
import pandas as pd
import networkx as nx
import seaborn as sns
import geopandas as gpd
import network_distance as nd
from functools import partial
from scipy.cluster import hierarchy
from matplotlib import pyplot as plt

nodes = pd.read_csv("fig_2_nodes.csv", sep = "\t")
edges = pd.read_csv("fig_2_edges.csv", sep = "\t")
province_order = nodes.drop(["occupation", "tot"], axis = 1).columns

G = nx.Graph()
G.add_nodes_from(nodes["occupation"].sort_values())
G.add_edges_from(list(edges[["src", "trg"]].itertuples(index = False)))
G = nx.convert_node_labels_to_integers(G)

node_attrs = nodes.sort_values(by = "occupation")[province_order].values
tensor = nd._make_tensor(G, node_attrs)
tensor.x /= tensor.x.sum(axis = 0)

Q_gpu = nd._ge_Q_gpu(tensor)
ge_gpu = nd._ge_gpu(Q_gpu, tensor.x[:,0], tensor.x[:,1])
distances_gpu = nd._pairwise_gpu(tensor.x.T, metric = partial(nd._ge_gpu_batch, Q_gpu))
distances_cpu = pd.DataFrame(data = distances_gpu.cpu().numpy(), index = province_order, columns = province_order)

sim_matrix = (1 / np.exp(distances_cpu))

row_linkage = hierarchy.linkage(distances_cpu.values[np.triu_indices(distances_cpu.shape[0], k = 1)], optimal_ordering = True, method = "ward")
col_linkage = hierarchy.linkage(distances_cpu.values[np.triu_indices(distances_cpu.shape[0], k = 1)], optimal_ordering = True, method = "ward")
sns_plot = sns.clustermap(sim_matrix, row_linkage = row_linkage, col_linkage = col_linkage, cmap = "Reds_r", yticklabels = True, xticklabels = False)
plt.savefig("fig_s8.pdf")

# Adaptive cut (manual)
cluster_provinces = {
   -1: ["Syria", "Lusitania"],
   0: ["Aquitania", "Belgica", "Germania Inferior", "Germania Superior", "Britannia", "Macedonia"],
   1: ["Hispania Citerior", "Aemilia (Regio VIII)", "Etruria (Regio VII)", "Samnium (Regio IV)",
       "Umbria (Regio VI)", "Transpadana (Regio XI)", "Venetia et Histria (Regio X)",
       "Latium et Campania (Regio I)", "Narbonensis", "Lugdunensis", "Apulia et Calabria (Regio II)",
       "Numidia", "Africa Proconsularis", "Baetica", "Mauretania Caesariensis"],
   2: ["Picenum (Regio V)", "Noricum", "Pannonia Superior", "Moesia Superior", "Pannonia Inferior",
       "Dacia", "Moesia Inferior", "Dalmatia"],
   3: ["Mauretania Tingitana", "Raetia", "Liguria (Regio IX)", "Asia", "Sicilia"],
   4: ["Sardinia", "Galatia", "Achaia", "Bruttium et Lucania (Regio III)"]
}

gdf = gpd.read_file("../../data/economic_complexity/provinces/provinces.shp")
gdf["cluster"] = gdf["province"].map({province: cluster for cluster in cluster_provinces for province in cluster_provinces[cluster]}).fillna(-1)

gdf.to_file("fig_3.shp")
