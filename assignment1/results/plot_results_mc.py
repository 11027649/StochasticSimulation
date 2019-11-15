import pandas
import matplotlib.pyplot as plt
import numpy as np
import time
import seaborn as sns
sns.set()

import math

df = pandas.read_csv("../data/mc_2000.csv", header=0)
df.columns = ["iterations", "samples", "area", "computationtime"]
df_new = df.loc[df['iterations'] == 2000]

total_points = np.arange(1000, 100000, 1000)

means = []
variances = []
computation_times = []

for points in total_points:
    mean = df_new[df_new['samples'] == points]['area'].mean()
    means.append(mean)
    var = df_new[df_new['samples'] == points]['area'].var()
    variances.append(var)
    computation_times.append(df_new[df_new['samples'] == points]['computationtime'].sum()/60)

    # compute confidence interval
    # if points % 10000 == 0 or points == 1000:
    #     print(points)
    #     lower = mean - 1.96 * math.sqrt(var)/math.sqrt(points)
    #     upper = mean + 1.96 * math.sqrt(var)/math.sqrt(points)
    #     print("Confidence interval: [", lower, ", ", upper, "]")
    #     print(mean, " ", mean - lower)

plt.figure(figsize=(12, 6))

lowerlims = [means[i] - variances[i] for i in range(len(variances))]
upperlims = [means[i] + variances[i] for i in range(len(variances))]
plt.fill_between(total_points, lowerlims, upperlims, facecolor='red', alpha=0.5)

plt.title("Monte Carlo integration \nRandom sampling", size=25)
plt.xlabel("Amount of samples (darts)", size=18)
plt.ylabel("Area of the Mandelbrot set", size=18)
plt.xticks(size=13)
plt.yticks(size=13)

ax1 = plt.gca()
labels1 = ax1.plot(total_points, means, color="red", label="area")

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

ax2.set_ylabel('Computation Time (min)', size=18)  # we already handled the x-label with ax1
labels2 = ax2.plot(total_points, computation_times, label="time")

ax1.set_ylim(1.50, 1.52)
ax2.set_ylim(0, 30)

plots = labels1 + labels2
labs = [l.get_label() for l in plots]
ax1.legend(plots, labs, loc='lower right')

plt.savefig("../figures/samples/pure_random/mc_" + str(time.time()) + ".svg", format='svg')