"""
Script for an md longtail distribution
"""

import simpy
import random
import csv
import statistics as stats
import numpy as np

seed = 42                                   #een seed, waarom nied
mean_joblength = 1                          #average job length, we use exponential distribution to sample a random job length
rho = np.arange(0.800,0.999, 0.020)         #rho itself is not actually used, but gives the relation between servetime and T_inter. (10 steps)
capacity = [1,2,4]                          #our store has this many servers
sim_time = 10000                            #duration of simulation, not used

customers_in_line = []

#store
class Store():
    def __init__(self, env, capacity):
        self.env = env
        self.capacity = capacity
        self.resource = simpy.Resource(env, capacity)

    def serving(self, joblength):
        yield self.env.timeout(joblength)

#customers
class Customer():
    def __init__(self, env, name, joblength):
        self.env = env
        self.name = name
        self.joblength = joblength

    def get_help(self, env, store):
        """
        Request a service at the store, with a predetermined job length which decides who gets helped first
        """

        arrival = env.now
        customers_in_line.append(self.name)


        with store.resource.request() as req:
            yield req

            #we wait till he's helped
            enter = env.now
            customers_in_line.remove(self.name)

            yield env.process(store.serving(self.joblength))

            #happy customer leaves
            leave = env.now

            with open("data/mdlong_results.csv", 'a') as resultsFile:

                writer = csv.writer(resultsFile)
                global the_rho
                global a_of_s

                waitingtime = enter - arrival

                writer.writerow([a_of_s, the_rho, self.name, arrival, enter, leave, self.joblength, waitingtime, len(customers_in_line)])


def setup(env, rho, capacity):
    """
        This sets up the simpy environment using the store and customer classes. We generate a list of customers with a joblength from an exponential distr.,
        same for inter arrival time. The customers are prioritized by their joblength: Shortest job first.
    """

    store = Store(env, capacity)

    no = 0
    while True:
        x = np.random.random()
        if x < 0.75:
            joblength = random.expovariate(1)
            t_inter = random.expovariate(capacity*rho)
        else:
            joblength = random.expovariate(1/5)
            t_inter = random.expovariate(5*capacity*rho)


        customer = Customer(env, f'customer{no}', joblength)

        env.process(customer.get_help(env, store=store))
        yield env.timeout(t_inter)

        no+=1

def main():
    for n in capacity:
        global a_of_s
        a_of_s = n
        for load in rho:
            global the_rho
            the_rho = load
            for i in range(1):
                global run_number
                run_number = i

                random.seed(seed)

                env = simpy.Environment()
                env.process(setup(env, n, load))
                env.run(until=sim_time)

if __name__ == "__main__":
    main()
