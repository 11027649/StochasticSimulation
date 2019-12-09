import pandas as pd
import os



def batch(rho, capacity):
    df = pd.read_csv("../data/mm" + capacity + "_temp_results.csv")
    df.columns = ["name", "arrive", "waitingtime", "len_queue"]

    batches = []

    # divide the dataframe into 20 batches
    for i in range(20):
        batches.append(df[(df["arrive"] > i * 500 + 200) & (df["arrive"] < (i + 1) * 500)])

    # concatenate batches
    result = pd.concat(batches)

    # write mean to csvfile
    with open("data/mm1_means_" + str(capacity)  + "_results.csv", 'a') as resultsFile:
        writer = csv.writer(resultsFile)

        writer.writerow([rho, result["waitingtime"].mean(), result["len_queue"].mean()])

    os.remove("../data/mm" + capacity + "_temp_results.csv")

