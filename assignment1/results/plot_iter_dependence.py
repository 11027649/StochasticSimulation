import pandas
import matplotlib.pyplot as plt
import numpy as np
import time
import seaborn as sns
sns.set()


df_mc_ = pandas.read_csv("../data/bak/mc_iters.csv", header=0)
df_mc_.columns = ["iterations", "samples", "area", "computationtime"]

df_lhs_ = pandas.read_csv("../data/bak/lc_iters.csv", header=0)
df_lhs_.columns = ["iterations", "samples", "area", "computationtime"]


df_mc = df_mc_.loc[df_mc_['samples'] == 50000]
df_lhs = df_lhs_.loc[df_mc_['samples'] == 50000]

max_iterations = np.arange(100, 2500, 100)

means_mc, means_lhs = [], []
variances_mc, variances_lhs  = [], []

for iters in max_iterations:
    means_mc.append(df_mc[df_mc['iterations'] == iters]['area'].mean())
    variances_mc.append(df_mc[df_mc['iterations'] == iters]['area'].var())

    means_lhs.append(df_lhs[df_lhs['iterations'] == iters]['area'].mean())
    variances_lhs.append(df_lhs[df_lhs['iterations'] == iters]['area'].var())

print(variances_mc)

# plt.scatter(df_new['samples'], df_new['area'])
plt.figure(figsize=(8, 8))
plt.plot(max_iterations, means_mc, color="r", label="pure random")
plt.plot(max_iterations, means_lhs, color="green", label="latin hypercube")

plt.legend()

plt.title("Iteration dependence", size=25)
plt.xlabel("Amount of iterations", size=18)
plt.ylabel("Area of the Mandelbrot set", size=18)
plt.xticks(size=13)
plt.yticks(size=13)

plt.savefig("iterdependence.svg", format="svg")