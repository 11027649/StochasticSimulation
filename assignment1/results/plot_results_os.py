import pandas
import matplotlib.pyplot as plt
import numpy as np
import time
import seaborn as sns
sns.set()

# df = pandas.read_csv("results/latin_cube_integration_results.csv", header=0)
df = pandas.read_csv("../data/orthogonal_integration.csv")
print(df.head())
df.columns = ["iterations", "samples", "area", "computationtime"]
print(df.describe())


df_temp = df.loc[df['iterations'] == 2000]
df_new = df_temp.loc[df['samples'] < 120000]

print(df_new.describe())

total_points = np.arange(10, 320, 5) * np.arange(10, 320, 5)

# print(total_points)
means = []
variances = []

for points in total_points:
    means.append(df_new[df_new['samples'] == points]['area'].mean())
    print(len(df_new[df_new['samples'] == points]['area']))
    variances.append(df_new[df_new['samples'] == points]['area'].var())

plt.plot(total_points, means)
plt.title("Monte Carlo, orthogonal sampling")
lowerlims = [means[i] - variances[i] for i in range(len(variances))]
upperlims = [means[i] + variances[i] for i in range(len(variances))]
plt.fill_between(total_points, lowerlims, upperlims, facecolor='blue', alpha=0.5)
plt.xlabel("Amount of samples (darts)")
plt.ylabel("Area of the Mandelbrot set")
plt.ylim(1.50, 1.52)
plt.xlim(0, 10000)
plt.savefig("os_" + str(time.time()) + ".png")