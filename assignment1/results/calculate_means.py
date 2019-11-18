import pandas
import matplotlib.pyplot as plt
import numpy as np
import time
import seaborn as sns
sns.set()

import math

df1 = pandas.read_csv("../data/antithetic_orthogonal_2000_100.csv", header=0)
df1.columns = ["iterations", "samples", "area1", "area2", "computationtime"]

df2 = df1.loc[df1['iterations'] == 2000]
print(df2.describe())
df = df2.loc[df2['samples'] == 10000]
df = df.head(n=2500)

df['area'] = 0.5 * (df['area1'] + df['area2'])

print(len(df))
print("mean", df['area'].mean())
print("std", df['area'].std())
print("var", df['area'].var())
print("mean time", df['computationtime'].mean())
print("sum time", df['computationtime'].sum()/60)
