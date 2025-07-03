import numpy as np
import pandas as pd

def randomize(mcp):
   col_sums = mcp.sum(axis = 0)
   row_sums = mcp.sum(axis = 1)
   mcp_random = np.random.uniform(size = mcp.shape)
   mcp_random[(mcp == 0)[np.random.permutation(mcp.columns)]] = 0 # With this we enforce the number of zeros in a province to be the same
   for _ in range(100):
      mcp_random = (mcp_random.T * np.nan_to_num((col_sums / mcp_random.sum(axis = 0)).values[:,np.newaxis])).T
      mcp_random = (mcp_random * np.nan_to_num((row_sums / mcp_random.sum(axis = 1)).values[:,np.newaxis]))
   return pd.DataFrame(mcp_random)

def nestedness(mcp, write = False):
   mcp_binary = mcp > 0
   isocline = mcp_binary.sum(axis = 1)
   if write:
      isocline.reset_index().to_csv(f"fig_s5_{write}.csv", sep = "\t", index = False, header = False)
   size_left = isocline.sum() / (mcp.shape[0] * mcp.shape[1])
   sum_left = 0
   for i in range(isocline.shape[0]):
      sum_left += mcp.iloc[i].values[:isocline[i] + 1].sum()
   return (sum_left / mcp.sum().sum()) / size_left

mcp = pd.read_csv("fig_1_b.csv", sep = "\t", header = None)
obs_nestedness = nestedness(mcp, write = "latin")
random_nestednesses = np.array([nestedness(randomize(mcp)) for _ in range(1000)])
np.savetxt("fig_s6_latin.csv", random_nestednesses, fmt = "%.6f")
p_value = (random_nestednesses >= obs_nestedness).sum() / random_nestednesses.shape[0]

print("============ Only Latin ================")
print(f"Nestedness of bias-corrected matrix (-1 = bottom-right nested, 0 = not nested, 1 = top-left nested): {obs_nestedness:.4f}")
print(f"Randomized Nestedness: mean = {random_nestednesses.mean():.4f}; std = {random_nestednesses.std():.4f}; p-value of observation > random = {p_value}")
print("========================================")

mcp = pd.read_csv("fig_1_a.csv", sep = "\t", header = None)
obs_nestedness = nestedness(mcp)
random_nestednesses = np.array([nestedness(randomize(mcp)) for _ in range(1000)])
p_value = (random_nestednesses >= obs_nestedness).sum() / random_nestednesses.shape[0]

print("============ Only Latin ================")
print(f"Nestedness of pre-correction matrix (-1 = bottom-right nested, 0 = not nested, 1 = top-left nested): {nestedness(mcp):.4f}")
print(f"Randomized Nestedness: mean = {random_nestednesses.mean():.4f}; std = {random_nestednesses.std():.4f}; p-value of observation > random = {p_value}")
print("========================================")

mcp = pd.read_csv("fig_s1_bottom.csv", sep = "\t", header = None)
obs_nestedness = nestedness(mcp, write = "all")
random_nestednesses = np.array([nestedness(randomize(mcp)) for _ in range(1000)])
np.savetxt("fig_s6_all.csv", random_nestednesses, fmt = "%.6f")
p_value = (random_nestednesses >= obs_nestedness).sum() / random_nestednesses.shape[0]

print("============ All Provinces ================")
print(f"Nestedness of bias-corrected matrix (-1 = bottom-right nested, 0 = not nested, 1 = top-left nested): {obs_nestedness:.4f}")
print(f"Randomized Nestedness: mean = {random_nestednesses.mean():.4f}; std = {random_nestednesses.std():.4f}; p-value of observation > random = {p_value}")
print("===========================================")

mcp = pd.read_csv("fig_s1_top.csv", sep = "\t", header = None)
obs_nestedness = nestedness(mcp)
random_nestednesses = np.array([nestedness(randomize(mcp)) for _ in range(1000)])
p_value = (random_nestednesses >= obs_nestedness).sum() / random_nestednesses.shape[0]

print("============ All Provinces ================")
print(f"Nestedness of pre-correction matrix (-1 = bottom-right nested, 0 = not nested, 1 = top-left nested): {nestedness(mcp):.4f}")
print(f"Randomized Nestedness: mean = {random_nestednesses.mean():.4f}; std = {random_nestednesses.std():.4f}; p-value of observation > random = {p_value}")
print("===========================================")
