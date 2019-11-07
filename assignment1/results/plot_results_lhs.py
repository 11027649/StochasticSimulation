import pandas
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns
sns.set()

df = pandas.read_csv("results/latin_cube_integration_results.csv", header=0)
print(df.head())
df.columns = ["iterations", "samples", "area", "computationtime"]
print(df.describe())


df_new = df.loc[df['iterations'] == 1000]
print(df_new.describe())

total_points = np.arange(1000, 100000, 1000)

means = []
variances = []

for points in total_points:
    print(points, " ",df_new[df_new['samples'] == points]['area'].var())
    means.append(df_new[df_new['samples'] == points]['area'].mean())
    variances.append(df_new[df_new['samples'] == points]['area'].var())

# plt.scatter(df_new['samples'], df_new['area'])
plt.plot(total_points, means)
plt.title("Latin Hypercube integration")
lowerlims = [means[i] - variances[i] for i in range(len(variances))]
upperlims = [means[i] + variances[i] for i in range(len(variances))]
plt.fill_between(total_points, lowerlims, upperlims, facecolor='blue', alpha=0.5)
plt.xlabel("Amount of samples (darts)")
plt.ylabel("Area of the Mandelbrot set")
plt.savefig("lhc.png")