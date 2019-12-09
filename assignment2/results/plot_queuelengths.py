import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from statistics import is_significant
import math

sns.set()

queue_types = ["mm1", "mm2", "mm4", "md1", "md2", "md4", "sjf1", "sjf2", "sjf4", "mlt1", "mlt2", "mlt4"]
#

saved_means = {}
stds = {}

for queue_type in queue_types:
    df = pd.read_csv("../data/" + queue_type + "_means_results.csv")
    try:
        df.columns = ["rho", "waitingtime", "len_queue"]
    except ValueError:
        df.columns = ["rho", "batchno", "waitingtime", "len_queue"]

    rhos = [0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.7, 0.75, 0.8, 0.85, 0.90, 0.95]
    print(rhos)

    plt.figure()
    means_per_rho = []
    stds_per_rho = []

    for rho in rhos:
        print("queue: ", queue_type, "rho: ", rho)

        # abs(f1 - f2) <= allowed_error
        # print(df[(df["rho"] == rho) & (df["sim_no"] == i)].describe())
        mean = df[df["rho"] == rho]["len_queue"].mean()
        std = df[df["rho"] == rho]["len_queue"].std()

        plt.scatter(rho, mean)
        plt.title("Queue lenghts for queue type: " + queue_type)
        plt.ylabel("Average queue length")
        plt.xlabel("Workload (rho)")

        means_per_rho.append(mean)
        stds_per_rho.append(std)


    plt.plot(rhos, means_per_rho)
    saved_means[queue_type] = means_per_rho
    stds[queue_type] = stds_per_rho

    plt.savefig("../figures/" + queue_type + "_results.png")

########################################### PLOT MMn
plt.figure(figsize=(10,8))
plt.plot(rhos, saved_means["mm1"], label="M/M/1 queue", color="firebrick")

z_star = 2.576
sample_sqrt = math.sqrt(len(saved_means["mm1"]))

plt.fill_between(rhos,
                        [saved_means["mm1"][i] - z_star * stds["mm1"][i] / sample_sqrt for i in range(len(saved_means["mm1"]))],
                        [saved_means["mm1"][i] + z_star * stds["mm1"][i] / sample_sqrt for i in range(len(saved_means["mm1"]))],
                        facecolor="firebrick",
                        alpha=0.5)


plt.plot(rhos, saved_means["md1"], label="M/D/1 queue", color="green")

sample_sqrt = math.sqrt(len(saved_means["md1"]))

plt.fill_between(rhos,
                        [saved_means["md1"][i] - z_star * stds["md1"][i] / sample_sqrt for i in range(len(saved_means["md1"]))],
                        [saved_means["md1"][i] + z_star * stds["md1"][i] / sample_sqrt for i in range(len(saved_means["md1"]))],
                        facecolor="green",
                        alpha=0.5)

plt.plot(rhos, saved_means["sjf1"], label="SJF1 queue", color="blue")
sample_sqrt = math.sqrt(len(saved_means["sjf1"]))
plt.fill_between(rhos,
                        [saved_means["sjf1"][i] - z_star * stds["sjf1"][i] / sample_sqrt for i in range(len(saved_means["sjf1"]))],
                        [saved_means["sjf1"][i] + z_star * stds["sjf1"][i] / sample_sqrt for i in range(len(saved_means["sjf1"]))],
                        facecolor="blue",
                        alpha=0.5)

plt.plot(rhos, saved_means["mlt1"], label="M/LT/1 queue", color="purple")
sample_sqrt = math.sqrt(len(saved_means["mlt1"]))
plt.fill_between(rhos,
                        [saved_means["mlt1"][i] - z_star * stds["mlt1"][i] / sample_sqrt for i in range(len(saved_means["mlt1"]))],
                        [saved_means["mlt1"][i] + z_star * stds["mlt1"][i] / sample_sqrt for i in range(len(saved_means["mlt1"]))],
                        facecolor="purple",
                        alpha=0.5)


plt.legend(prop={'size': 18})
plt.xticks(size=15)
plt.yticks(size=15)
plt.title("Queue lengths for all experiments with 1 server", size=25)
plt.ylabel("Average queue length", size=18)
plt.xlabel("Workload ($\\rho$)", size=18)
plt.savefig("../figures/all_lengths.svg", format="svg")