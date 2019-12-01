"""
Script to simulate an M/M/1 and M/M/n queues using simpy.
"""
import sys
import pandas as pd
import os

import simpy
import random
import csv
import numpy as np

# seed = 42                               # dit is een seed
mean_joblength = 1                      # Minutes it takes to serve, either fixed or from distribution (known as mu)
sim_time = 10000                        # Simulation time in minutes

customers_in_line = []

class Store(object):
    """A Store has a limited number of cashiers (``SERVERS``) to
    help customers.

    Customers request a server. When there is no queue, they go to a server which takes joblength to help.

    """
    def __init__(self, env, capacity):
        self.env = env
        self.capacity = capacity
        self.resource = simpy.Resource(env, capacity)

    def serving(self, joblength):
        """yield timeout for servicing a customer"""

        yield self.env.timeout(joblength)

class Customer():
    def __init__(self, env, name, joblength):
        self.env = env
        self.name = name
        self.joblength = joblength

    def get_help(self, env, run, rho, store):
        """
        Request a service at the store, predetermined joblength. FIFO system
        """

        arrival = env.now
        customers_in_line.append(self.name)

        with store.resource.request() as req:
            yield req

            #we wait till he's helped
            enter = env.now
            customers_in_line.remove(self.name)

            yield env.process(store.serving(self.joblength))

            leave = env.now

            with open("data/mlt" + str(store.capacity)  + "_temp.csv", 'a') as resultsFile:
                writer = csv.writer(resultsFile)

                # we are interested in the waiting time of the customers
                waitingtime = enter - arrival

                writer.writerow([arrival, waitingtime, len(customers_in_line)])

def setup(env, run, rho, capacity):
    """
    Create a store and generate customers while simulation is running.
    T_inter is dependent on joblength in order to keep workload the same.
    """

    # Create the store
    store = Store(env, capacity)

    customer_no = 0

    # stop at a certain simulation time
    while True:
        # 75% of the time around 1, 25% of the time around 5

        #old loop
        # x = np.random.random()
        # if x < 0.75:
        #     joblength = random.expovariate(1)
        #     t_inter = random.expovariate(capacity*rho)
        # else:
        #     joblength = random.expovariate(1/5)
        #     t_inter = random.expovariate(5*capacity*rho)

        #new loop
        x = np.random.random()
        if x < 0.75:
            joblength = random.expovariate(1)
        else:
            joblength = random.expovariate(1/5)

        t_inter = random.expovariate(rho*capacity*0.8)

        customer = Customer(env, f'customer{customer_no}', joblength)

        env.process(customer.get_help(env, run=run, rho=rho, store=store))
        yield env.timeout(t_inter)
        customer_no += 1

def batch(rho, capacity):
    df = pd.read_csv("data/mlt" + str(capacity) + "_temp.csv")
    df.columns = ["arrive", "waitingtime", "len_queue"]

    # divide the dataframe into 20 batches
    for batch in range(20):
        df[(df["arrive"] > batch * 500 + 200) & (df["arrive"] < (batch + 1) * 500)]["waitingtime"].mean()

        # write mean to csvfile
        with open("data/mlt" + str(capacity)  + "_means_results.csv", 'a') as resultsFile:
            writer = csv.writer(resultsFile)

            writer.writerow([rho, batch,
                                df[(df["arrive"] > batch * 500 + 200) & (df["arrive"] < (batch + 1) * 500)]["waitingtime"].mean(),
                                df[(df["arrive"] > batch * 500 + 200) & (df["arrive"] < (batch + 1) * 500)]["len_queue"].mean()])

    os.remove("data/mlt" + str(capacity) + "_temp.csv")

def main():

    if not len(sys.argv) == 4:
        print("Usage python mmn_queue.py <capacity> <rho> <run number>")

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