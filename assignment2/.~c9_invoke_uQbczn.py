import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("des_results.csv")
df.columns = ["run_number", "name", "arrive", "enter", "leave"]
df["waiting"] = df["enter"] - df["arrive"]
df["serving"] = df["leave"] - df["enter"]

print(df.describe())

plt.hist(df["waiting"])
plt.savefig("waiting_hist.png")

plt.figure()
plt.hist(df["serving"])
plt.savefig("serving_hist.png")


















































