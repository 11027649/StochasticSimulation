import pandas
import matplotlib.pyplot as plt
import numpy as np
import time
import seaborn as sns
sns.set()

df = pandas.read_csv("../data/mc_2000.csv", header=0)
print(df.head())
df.columns = ["iterations", "samples", "area", "computationtime"]
print(df.describe())


df_new = df.loc[df['iterations'] == 2000]
print(df_new.describe())

total_points = np.arange(1000, 100000, 1000)
print(len(total_points))

means = []
variances = []

for points in total_points:
    means.append(df_new[df_new['samples'] == points]['area'].mean())
    variances.append(df_new[df_new['samples'] == points]['area'].var())

# plt.scatter(df_new['samples'], df_new['area'])
plt.figure(figsize=(8, 8))
plt.plot(total_points, means, color="red")

lowerlims = [means[i] - variances[i] for i in range(len(variances))]
upperlims = [means[i] + variances[i] for i in range(len(variances))]
plt.fill_between(total_points, lowerlims, upperlims, facecolor='red', alpha=0.5)


# PLOT antithetic
df = pandas.read_csv("../data/antithetic_mc.csv", header=0)
df.columns = ["iterations", "samples", "area", "computationtime"]

df_new = df.loc[df['iterations'] == 2000]

means_a = []
variances_a = []

for points in total_points:
    means_a.append(df_new[df_new['samples'] == points]['area'].mean())
    variances_a.append(df_new[df_new['samples'] == points]['area'].var())

plt.plot(total_points, means_a, color="green")

print(means_a, means)

lowerlims_a = [means_a[i] - variances_a[i] for i in range(len(variances_a))]
upperlims_a = [means_a[i] + variances_a[i] for i in range(len(variances_a))]
plt.fill_between(total_points, lowerlims_a, upperlims_a, facecolor='green', alpha=0.5)

plt.title("Monte Carlo integration \nRandom sampling with antithetic variables", size=20)
plt.xlabel("Amount of samples (darts)", size=15)
plt.ylabel("Area of the Mandelbrot set", size=15)
plt.xticks(size=10)
plt.yticks(size=10)

plt.ylim(1.50, 1.52)
plt.xlim(0,50000)

plt.savefig("mc_antithetic" + str(time.time()) + ".png")