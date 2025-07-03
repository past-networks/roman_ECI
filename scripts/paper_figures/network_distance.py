import torch, torch_geometric
import numpy as np
import networkx as nx
from scipy.sparse import csgraph
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score, pairwise_distances

device = "cuda" if torch.cuda.is_available() else "cpu"

def _make_tensor(G, observations):
   edge_index = [[], []]
   for edge in G.edges:
      edge_index[0].append(edge[0])
      edge_index[1].append(edge[1])
      edge_index[0].append(edge[1])
      edge_index[1].append(edge[0])
   edge_index = torch.tensor(edge_index, dtype = torch.long).to(device)
   x = torch.tensor(observations, dtype = torch.double).to(device)
   tensor = torch_geometric.data.Data(x = x, edge_index = edge_index)
   return tensor

def _ge(Q, src, trg):
   diff = src - trg
   return np.sqrt(diff.T.dot(Q.dot(diff)))

def _ge_Q(G):
   A = nx.adjacency_matrix(G).todense().astype(float)
   return np.linalg.pinv(csgraph.laplacian(np.matrix(A), normed = False))

def _ge_gpu(Q, src, trg):
   diff = src - trg
   return torch.sqrt(torch.matmul(diff, torch.matmul(Q, diff)))

def _ge_gpu_batch(Q, src, trg):
   diff = src - trg
   return torch.sqrt((diff * torch.matmul(Q, diff.T).T).sum(dim = 1))

def _ge_Q_gpu(tensor):
   L_ei, Lew = torch_geometric.utils.get_laplacian(tensor.edge_index)
   L = torch_geometric.utils.to_dense_adj(edge_index = L_ei, edge_attr = Lew)[0]
   return torch.linalg.pinv(L, hermitian = True).double()

def _pairwise(X, metric = "euclidean"):
   return pairwise_distances(X, metric = metric)

def _pairwise_gpu(X, metric = None):
   if metric is None:
      return torch.cdist(X, X)
   else:
      out = torch.zeros((X.shape[0], X.shape[0])).to(device)
      for i in range(X.shape[0]):
         out[i,i + 1:] = metric(X[i], X[(i + 1):])
      out = out + out.T
      return out

def cluster(distance_matrix, min_samples = 2):
   np.fill_diagonal(distance_matrix, 0)
   clusters = []
   for eps in np.linspace(distance_matrix[distance_matrix > 0].min(), distance_matrix.mean(), num = 50):
      cluster = DBSCAN(eps = eps, min_samples = min_samples, metric = "precomputed").fit(distance_matrix)
      if len(set(cluster.labels_)) > 1:
         clusters.append((cluster, silhouette_score(distance_matrix, cluster.labels_, metric = "precomputed")))
      else:
         clusters.append((cluster, -1))
   return max(clusters, key = lambda x: x[1])[0].labels_