import pandas
import matplotlib.pyplot as plt
import numpy as np
import time
import seaborn as sns
sns.set()

import math


filenames = ["../data/random.csv",
            "../data/antithetic_random_2000_100.csv",
            "../data/latin_hypercube.csv",
            "../data/antithetic_latin_hypercube_2000_100.csv",
            "../data/orthogonal_integration.csv",
            "../data/antithetic_orthogonal_2000_100.csv"]
heights = []

for file in filenames:
    print(file)
    try:
        df1 = pandas.read_csv(file, header=0)

        if "antithetic" in file:
            df1.columns = ["iterations", "samples", "area1", "area2", "computationtime"]

            # print(df1.describe())
            df1['area'] = 0.5 * (df1['area1'] + df1['area2'])
        else:
            df1.columns = ["iterations", "samples", "area", "computationtime"]

        df2 = df1.loc[df1['iterations'] == 2000]
        df = df2.loc[df2['samples'] == 10000]
        df = df.head(n=2500)

        print(len(df))

        heights.append(df['area'].var())


    except FileNotFoundError as e:
        print(e)

print(heights)
plt.figure(figsize=(12, 6))
plt.title("Variances Monte Carlo integration methods\n runs=2500, iterations=2000, samples=10000", size=25)
plt.bar(range(len(heights)), heights, width=0.6, color="r")
plt.xticks(range(len(heights)), ["random", "random anti", "lh", "lh anti", "ortho", "ortho anti"], size=18)
plt.yticks(size=13)
plt.xlabel("Sampling methods", size=18)
plt.ylabel("Variance", size=18)

# ax = plt.gca()

# for rect, label in zip(ax.patches, heights):
#     print(rect, label)
#     height = rect.get_height()
#     ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label)

plt.savefig("bargraph.svg", format="svg")

