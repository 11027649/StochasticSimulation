import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from statistics import is_significant

sns.set()

queue_types = ["mm1", "mm2", "mm4", "md1", "md2", "md4", "mlt1", "mlt2", "mlt4", "sjf1", "sjf2", "sjf4"]
#

saved_means = {}
stds = {}

for queue_type in queue_types:
    df = pd.read_csv("../data/" + queue_type + "_means_results.csv")
    df.columns = ["rho", "waitingtime", "len_queue"]

    rhos = [0.05, 0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.7, 0.75, 0.8, 0.85, 0.90, 0.95]
    print(rhos)

    plt.figure()
    means_per_rho = []

    for rho in rhos:
        print("queue: ", queue_type, "rho: ", rho)

        # abs(f1 - f2) <= allowed_error
        # print(df[(df["rho"] == rho) & (df["sim_no"] == i)].describe())
        mean = df[df["rho"] == rho]["waitingtime"].mean()
        std = df[df["rho"] == rho]["waitingtime"].std()

        plt.scatter(rho, mean)
        plt.title("Waiting times for queue type: " + queue_type)
        plt.ylabel("Average waitingtime")
        plt.xlabel("Workload (rho)")

        means_per_rho.append(mean_per_rho)
        stds_per_rho.append(std)


    plt.plot(rhos, means_per_rho)
    saved_means[queue_type] = means_per_rho
    stds[queue_type] = stds_per_rho

    plt.savefig("../figures/" + queue_type + "_results.png")


plt.figure(figsize=(10,8))
plt.plot(rhos, saved_means["mm1"], label="M/M/1 queue", color="firebrick")
plt.plot(rhos, saved_means["mm2"], label="M/M/2 queue", color="goldenrod")
plt.plot(rhos, saved_means["mm4"], label="M/M/4 queue", color="forestgreen")

z_star = 2.576
sample_sqrt = math.sqrt(len(saved_means["mm1"]))
plt.fill_between(rhos, 
                        [means_per_rho["mm1"][i] - z_star * stds["mm1"][i] /sample_sqrt for i in range(len(saved_means["mm1"]))],
                        [means_per_rho ], facecolor="firebrick")

plt.legend(prop={'size': 18})
plt.xticks(size=15)
plt.yticks(size=15)
plt.title("Waiting times for M/M/n queue\n with different amounts of servers and workload", size=25)
plt.ylabel("Average waitingtime", size=18)
plt.xlabel("Workload ($\\rho$)", size=18)
plt.savefig("test.png")
# plt.savefig("../figures/mmn_all.svg", format="svg")



# plt.figure(figsize=(10,8))
# plt.plot(rhos, saved_means["sjf1"], label="SJF1 queue", color="firebrick")
# plt.plot(rhos, saved_means["sjf2"], label="SJF2 queue", color="goldenrod")
# plt.plot(rhos, saved_means["sjf4"], label="SJF4 queue", color="forestgreen")
# plt.legend(prop={'size': 18})
# plt.xticks(size=15)
# plt.yticks(size=15)
# plt.title("Waiting times for Shortest Job First queue\n with different amounts of servers and workload", size=25)
# plt.ylabel("Average waitingtime", size=18)
# plt.xlabel("Workload ($\\rho$)", size=18)
# plt.savefig("../figures/sjf_all.svg", format="svg")
# plt.savefig("../figures/sjf_all.png")



# plt.figure(figsize=(10,8))
# plt.plot(rhos, saved_means["md1"], label="M/D/1 queue", color="firebrick")
# plt.plot(rhos, saved_means["md2"], label="M/D/2 queue", color="goldenrod")
# plt.plot(rhos, saved_means["md4"], label="M/D/4 queue", color="forestgreen")
# plt.legend(prop={'size': 18})
# plt.xticks(size=15)
# plt.yticks(size=15)
# plt.title("Waiting times for M/D/n queue\n with different amounts of servers and workload", size=25)
# plt.ylabel("Average waitingtime", size=18)
# plt.xlabel("Workload ($\\rho$)", size=18)
# plt.savefig("../figures/mdn_all.svg",  format="svg")



# plt.figure(figsize=(10,8))
# plt.plot(rhos, saved_means["mlt1"], label="M/LT/1 queue", color="firebrick")
# plt.plot(rhos, saved_means["mlt2"], label="M/LT/2 queue", color="goldenrod")
# plt.plot(rhos, saved_means["mlt4"], label="M/LT/4 queue", color="forestgreen")
# plt.legend(prop={'size': 18})
# plt.xticks(size=15)
# plt.yticks(size=15)
# plt.title("Waiting times for M/LT/n queue\n with different amounts of servers and workload", size=25)
# plt.ylabel("Average waitingtime", size=18)
# plt.xlabel("Workload ($\\rho$)", size=18)
# plt.savefig("../figures/mltn_all.svg",  format="svg")