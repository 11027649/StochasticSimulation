import simpy
import random

env = simpy.Environment()
res = simpy.PriorityResource(env, capacity = 1)

def print_stats(res):
    print(f'{res.count} of {res.capacity} slots are allocated.')
    print(' Users:', res.users)
    print(' Queued events:', res.queue)
    print(env.now)

def user(res):
    print_stats(res)
    with res.request() as req:
        yield req
        print_stats(res)
    print_stats(res)

procs = [env.process(user(res)) for i in range(10)]
env.run()