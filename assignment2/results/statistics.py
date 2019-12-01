import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import math


def main():
    plot_mmn()
    plot_sjf()
    plot_mdn()
    plot_lt()

def plot_sjf():
    df1 = pd.read_csv("../data/sjf1_means_results.csv")
    df2 = pd.read_csv("../data/sjf2_means_results.csv")
    df3 = pd.read_csv("../data/sjf4_means_results.csv")
    df1.columns = ["rho", "avgwaiting", "avglength"]
    df2.columns = ["rho", "avgwaiting", "avglength"]
    df3.columns = ["rho","avgwaiting", "avglength"]

    alpha = 0.01
    # rhos = [0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.7, 0.75, 0.8, 0.85, 0.90, 0.95]
    rhos = [0.1, 0.20,0.30,0.40, 0.50,0.60, 0.7, 0.8, 0.90]
    bieb = {}
    bieb["1-2"] = []
    bieb["2-4"] = []
    bieb["1-4"] = []

    plt.figure(figsize=(10,6))

    for rho in rhos:
        significant, iterations = is_significant(df1, df2, rho, alpha)
        bieb["1-2"].append(iterations)
        if (significant):

            plt.scatter(rho, iterations, color="green")

        significant, iterations = is_significant(df2, df3, rho, alpha)
        bieb["2-4"].append(iterations)
        if (significant):

            plt.scatter(rho, iterations, color="blue")

        significant, iterations = is_significant(df1, df3, rho, alpha)
        bieb["1-4"].append(iterations)

        if (significant):

            plt.scatter(rho, iterations, color="purple")

    plt.plot(rhos, bieb["1-2"], color="green", label="1-2")
    plt.plot(rhos, bieb["2-4"], color="blue", label="2-4")
    plt.plot(rhos, bieb["1-4"], color="purple", label="1-4")
    plt.legend(prop={'size': 18})
    plt.title("Statistical significance M/M/n priority scheduling queue", size=25)
    plt.xticks(size=15)
    plt.yticks(size=15)
    plt.xlabel("$\\rho$", size=18)
    plt.ylabel("Number of batches", size=18)

    plt.savefig("significance_sjf.svg", format="svg")


def plot_mdn():
    df1 = pd.read_csv("../data/md1_means_results.csv")
    df2 = pd.read_csv("../data/md2_means_results.csv")
    df3 = pd.read_csv("../data/md4_means_results.csv")
    df1.columns = ["rho", "avgwaiting", "avglength"]
    df2.columns = ["rho", "avgwaiting", "avglength"]
    df3.columns = ["rho","avgwaiting", "avglength"]

    alpha = 0.01
    # rhos = [0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.7, 0.75, 0.8, 0.85, 0.90, 0.95]
    rhos = [0.1, 0.20,0.30,0.40, 0.50,0.60, 0.7, 0.8, 0.90]
    bieb = {}
    bieb["1-2"] = []
    bieb["2-4"] = []
    bieb["1-4"] = []

    plt.figure(figsize=(10,6))

    for rho in rhos:
        significant, iterations = is_significant(df1, df2, rho, alpha)
        bieb["1-2"].append(iterations)
        if (significant):

            plt.scatter(rho, iterations, color="green")

        significant, iterations = is_significant(df2, df3, rho, alpha)
        bieb["2-4"].append(iterations)
        if (significant):

            plt.scatter(rho, iterations, color="blue")

        significant, iterations = is_significant(df1, df3, rho, alpha)
        bieb["1-4"].append(iterations)

        if (significant):

            plt.scatter(rho, iterations, color="purple")

    plt.plot(rhos, bieb["1-2"], color="green", label="1-2")
    plt.plot(rhos, bieb["2-4"], color="blue", label="2-4")
    plt.plot(rhos, bieb["1-4"], color="purple", label="1-4")
    plt.legend(prop={'size': 18})
    plt.title("Statistical significance M/D/n queue", size=25)
    plt.xticks(size=15)
    plt.yticks(size=15)
    plt.xlabel("$\\rho$", size=18)
    plt.ylabel("Number of batches", size=18)

    plt.savefig("significancemdn.svg", format="svg")


def plot_mmn():
    df1 = pd.read_csv("../data/mm1_means_results.csv")
    df2 = pd.read_csv("../data/mm2_means_results.csv")
    df3 = pd.read_csv("../data/mm4_means_results.csv")
    df1.columns = ["rho", "avgwaiting", "avglength"]
    df2.columns = ["rho", "avgwaiting", "avglength"]
    df3.columns = ["rho","avgwaiting", "avglength"]

    alpha = 0.01
    # rhos = [0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.7, 0.75, 0.8, 0.85, 0.90, 0.95]
    rhos = [0.1, 0.20,0.30,0.40, 0.50,0.60, 0.7, 0.8, 0.90]
    bieb = {}
    bieb["1-2"] = []
    bieb["2-4"] = []
    bieb["1-4"] = []

    plt.figure(figsize=(10,6))

    for rho in rhos:
        significant, iterations = is_significant(df1, df2, rho, alpha)
        bieb["1-2"].append(iterations)
        if (significant):

            plt.scatter(rho, iterations, color="green")

        significant, iterations = is_significant(df2, df3, rho, alpha)
        bieb["2-4"].append(iterations)
        if (significant):

            plt.scatter(rho, iterations, color="blue")

        significant, iterations = is_significant(df1, df3, rho, alpha)
        bieb["1-4"].append(iterations)

        if (significant):

            plt.scatter(rho, iterations, color="purple")

    plt.plot(rhos, bieb["1-2"], color="green", label="1-2")
    plt.plot(rhos, bieb["2-4"], color="blue", label="2-4")
    plt.plot(rhos, bieb["1-4"], color="purple", label="1-4")
    plt.legend(prop={'size': 18})
    plt.title("Statistical significance M/M/n queue", size=25)
    plt.xticks(size=15)
    plt.yticks(size=15)
    plt.xlabel("$\\rho$", size=18)
    plt.ylabel("Number of batches", size=18)

    plt.savefig("significancemmn.svg", format="svg")


def plot_lt():
    df1 = pd.read_csv("../data/mlt1_means_results.csv")
    df2 = pd.read_csv("../data/mlt2_means_results.csv")
    df3 = pd.read_csv("../data/mlt4_means_results.csv")
    df1.columns = ["rho", "batchno", "avgwaiting", "avglength"]
    df2.columns = ["rho", "batchno", "avgwaiting", "avglength"]
    df3.columns = ["rho", "batchno","avgwaiting", "avglength"]

    alpha = 0.01
    # rhos = [0.1, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.7, 0.75, 0.8, 0.85, 0.90, 0.95]
    rhos = [0.1, 0.20,0.30,0.40, 0.50,0.60, 0.7, 0.8, 0.90]
    bieb = {}
    bieb["1-2"] = []
    bieb["2-4"] = []
    bieb["1-4"] = []

    plt.figure(figsize=(10,6))

    for rho in rhos:
        significant, iterations = is_significant(df1, df2, rho, alpha)
        bieb["1-2"].append(iterations)
        if (significant):

            plt.scatter(rho, iterations, color="green")

        significant, iterations = is_significant(df2, df3, rho, alpha)
        bieb["2-4"].append(iterations)
        if (significant):

            plt.scatter(rho, iterations, color="blue")

        significant, iterations = is_significant(df1, df3, rho, alpha)
        bieb["1-4"].append(iterations)

        if (significant):

            plt.scatter(rho, iterations, color="purple")

    plt.plot(rhos, bieb["1-2"], color="green", label="1-2")
    plt.plot(rhos, bieb["2-4"], color="blue", label="2-4")
    plt.plot(rhos, bieb["1-4"], color="purple", label="1-4")
    plt.legend(prop={'size': 18})
    plt.title("Statistical significance M/LT/n queue", size=25)
    plt.xticks(size=15)
    plt.yticks(size=15)
    plt.xlabel("$\\rho$", size=18)
    plt.ylabel("Number of batches", size=18)

    plt.savefig("significancemlt.svg", format="svg")



def is_significant(df1, df2, rho, alpha):
    df1.dropna()
    df2.dropna()

    # calculate when statistic significance is reached between two datasets

    max_its = max(len(df1[(df1["rho"] == rho)]), len(df2[(df2["rho"] == rho)]))

    statistic_significance = False
    counter = 1

    while not statistic_significance:
        statistic, pvalue = stats.ttest_ind(df1[(df1["rho"] == rho)]["avgwaiting"][:counter], df2[(df2["rho"] == rho)]["avgwaiting"][:counter])

        if pvalue <= alpha:
            statistic_significance = True
        else:
            counter += 1

        if counter > max_its:
            break

    return statistic_significance, counter


    # uncertainty = 1.96 * batch_std / math.sqrt(len(df[(df["servers"] == 1) & (df["rho"] == 0.8)]["waiting"]))
    # print(uncertainty)
    # confidence_int_lb = batch_mean - uncertainty
    # confidence_int_ub = batch_mean + uncertainty

if __name__ == "__main__":
    main()
