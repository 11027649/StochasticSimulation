import simpy
import random
import csv
import statistics as stats

seed = 33               #een seed, waarom nied
customercount = 100     #amount of customers to make
initial_customers = 3   #customers who arrive at t = 0
customerslist = []      #customers chill in list
mean_joblength = 5      #average job length, we use exponential distribution to sample a random job length
t_inter = 8             #average inter arrival time, used in exponential distribution
capacity = 1            #our store has this many servers
sim_time = 100          #duration of simulation, not used

waits = []              #some lists for wait and joblengths
jobs = []               #used for some statistics after a simulation

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

    def get_help(self, env, store, joblength):
        """
        Request a service at the store, with a predetermined job length which decides who gets helped first
        """

        print(f'{self.name} arrives at the store at {env.now}.')
        arrival = env.now

        with store.resource.request(priority=self.joblength) as req:
            print(f'{self.name} requests help at {env.now} with job length {self.joblength}')
            yield req

            #we wait till he's helped
            print(f'{self.name} gets help at {env.now}, it will take {self.joblength}')
            enter = env.now
            waits.append(enter-arrival)
            yield env.process(store.serving(self.joblength))

            #happy customer leaves
            print(f'{self.name} leaves at {env.now}, goodbye')
            leave = env.now
            jobs.append(leave-enter)

            with open("sjf_results.csv", 'a') as resultsFile:
                writer = csv.writer(resultsFile)
                writer.writerow([self.name, arrival, enter, leave])


def setup(env):
    """
    This sets up the simpy environment using the store and customer classes. We generate a list of customers with a joblength from an exponential distr.,
    same for inter arrival time. The customers are prioritized by their joblength: Shortest job first.
    """

    for i in range(customercount):
        joblength = random.expovariate(1/mean_joblength)
        customer = Customer(env, f'customer{i}', joblength)
        customerslist.append(customer)

    store = Store(env, capacity)

    for customer in customerslist:
        env.process(customer.get_help(env, store = store, joblength = customer.joblength))
        yield env.timeout(random.expovariate(1/t_inter))

def setupshop():
    print(f"our shop is open, we have {capacity} server(s) ready")

def printstats(waits, jobs):
    print(f"""
    ================================================
    results are in:

    """)

    average_wait = stats.mean(waits)
    average_joblength = stats.mean(jobs)

    print(f"""
    the average waiting time is {average_wait}
    the average joblength is {average_joblength}
    """)

def main():

    random.seed(seed)

    env = simpy.Environment()

    setupshop()

    env.process(setup(env))

    env.run()

    printstats(waits,jobs)

if __name__ == "__main__":
    main()
