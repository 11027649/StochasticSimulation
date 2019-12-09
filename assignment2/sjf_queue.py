import sys
import pandas as pd
import os

import simpy
import random
import csv
import statistics as stats
import numpy as np

#seed = 42                          #een seed, waarom nied
mean_joblength = 1                  #average job length, we use exponential distribution to sample a random job length
sim_time = 10000                    #duration of simulation

customers_in_line = []

#store
class Store():
    def __init__(self, env, capacity):
        self.env = env
        self.capacity = capacity
        self.resource = simpy.PriorityResource(env, capacity=capacity)

    def serving(self, joblength):
        yield self.env.timeout(joblength)

#customers
class Customer():
    def __init__(self, env, name, joblength):
        self.env = env
        self.name = name
        self.joblength = joblength

    def get_help(self, env, run, rho, store):
        """
        Request a service at the store, with a predetermined job length which decides who gets helped first
        """
        arrival = env.now
        customers_in_line.append(self.name)

        with store.resource.request(priority=self.joblength) as req:
            yield req

            #we wait till he's helped
            enter = env.now
            customers_in_line.remove(self.name)

            yield env.process(store.serving(self.joblength))

            #happy customer leaves
            leave = env.now

            with open("data/sjf" + str(store.capacity) + "_temp.csv", 'a') as resultsFile:
                writer = csv.writer(resultsFile)

                waitingtime = enter - arrival

                writer.writerow([arrival, waitingtime, len(customers_in_line)])


def setup(env, run, rho, capacity):
    """
    This sets up the simpy environment using the store and customer classes. We generate a list of customers with a joblength from an exponential distr.,
    same for inter arrival time. The customers are prioritized by their joblength: Shortest job first.
    """

    store = Store(env, capacity)
    customer_no = 0

    while True:

        joblength = random.expovariate(mean_joblength)
        customer = Customer(env, f'customer{customer_no}', joblength)

        t_inter = random.expovariate(capacity*rho)

        env.process(customer.get_help(env, run=run, rho=rho, store=store))
        yield env.timeout(t_inter)
        customer_no+=1

def batch(rho, capacity):
    df = pd.read_csv("data/sjf" + str(capacity) + "_temp.csv")
    df.columns = ["arrive", "waitingtime", "len_queue"]

    # divide the dataframe into 20 batches
    for i in range(20):
        df[(df["arrive"] > i * 500 + 200) & (df["arrive"] < (i + 1) * 500)]["waitingtime"].mean()

        # write mean to csvfile
        with open("data/sjf" + str(capacity)  + "_means_results.csv", 'a') as resultsFile:
            writer = csv.writer(resultsFile)

            writer.writerow([rho,
                                df[(df["arrive"] > i * 500 + 200) & (df["arrive"] < (i + 1) * 500)]["waitingtime"].mean(),
                                df[(df["arrive"] > i * 500 + 200) & (df["arrive"] < (i + 1) * 500)]["len_queue"].mean()])

    os.remove("data/sjf" + str(capacity) + "_temp.csv")

def main():

    if not len(sys.argv) == 4:
        print("Usage python sjf_queue.py <capacity> <rho> <run number>")

    capacity = int(sys.argv[1])
    rho = float(sys.argv[2])
    run = int(sys.argv[3])

    # Setup and start the simulation
    # random.seed(seed)

    # Create an environment and start the setup process
    env = simpy.Environment()
    env.process(setup(env, run, rho, capacity))

    # Execute!
    env.run(until=sim_time)
    batch(rho, capacity)

if __name__ == "__main__":
    main()
