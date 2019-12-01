"""
Script to simulate an M/M/1 and M/M/n queues using simpy.
"""

import simpy
import random
import csv
import numpy as np

seed = 42                               # dit is een seed
mean_joblength = 1                      # Minutes it takes to serve, either fixed or from distribution (known as mu)
sim_time = 1000                        # Simulation time in minutes

customers_in_line = []
average_expo = []

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

    def get_help(self, env, store):
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

            with open("data/natasja.csv", 'a') as resultsFile:
                writer = csv.writer(resultsFile)
                global the_rho
                global a_of_s

                waitingtime = enter - arrival

                writer.writerow([self.name, arrival, enter, leave, self.joblength, waitingtime, len(customers_in_line)])

def setup(env, rho, capacity):
    """
    Create a store and generate customers while simulation is running.
    T_inter is dependent on joblength in order to keep workload the same.
    """

    # Create the store
    store = Store(env, capacity)

    no = 0

    while True:

        joblength = random.expovariate(mean_joblength)
        customer = Customer(env, f'customer{no}', joblength)

        no += 1

        t_inter = random.expovariate(3)
        average_expo.append(t_inter)
        print(no, env.now, t_inter)

        env.process(customer.get_help(env, store=store))
        yield env.timeout(t_inter)



def main():

    # mu
    load = 3

    # capacity/ servers
    n = 1

    # Setup and start the simulation
    random.seed(seed)

    # Create an environment and start the setup process
    env = simpy.Environment()
    env.process(setup(env, load, n))

    # Execute!
    env.run(until=sim_time)

    print("done")
    print(np.mean(average_expo))


if __name__ == "__main__":
    main()