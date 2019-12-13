from ParticleGrid import ParticleGrid
import matplotlib.pyplot as plt
import os
import math
import pickle
import sys
import copy
import random
from numba import jit

from helpers import visualize, plot_convergence_and_temp, save_best, grouper, mover, calc_score

def main():
    if not len(sys.argv) == 4:
        print("usage: python sa_particles.py <no of particles> <coolscheme> <forces y/n>")
        sys.exit(1)

    amount_of_particles = int(sys.argv[1])
    coolscheme = sys.argv[2]

    # sanity checks
    if not coolscheme in ["exponential", "linear", "reheat"]:
        print("pick one of \"exponential\", \"linear\", \"reheat\"")

    if sys.argv[3] not in ["y", "yes", "n", "no"]:
        print("pls say y, yes, n or no against a force field")

    max_iter = 100

    # instantiate configuration object
    configuration = ParticleGrid(amount_of_particles=amount_of_particles,
                            radius=1,
                            coolscheme=coolscheme,
                            steps=max_iter)


    configuration = run_sa(configuration)

    filename = "test.png"
    plot_convergence_and_temp(filename, configuration, coolscheme)
    print("done, best score: ", configuration.best_score)

def run_sa(configuration):

    step = 0

    # run the algorithm
    for step in range(configuration.steps):
        print("step: ", step, "score: ", configuration.score)

        # perform a step
        configuration = simannealing_step(configuration)

        # save the current score
        configuration.scores_list.append(configuration.score)

        # cool the system
        configuration.current_temp = configuration.temperatures[step]

    return configuration



def simannealing_step(configuration):
    """ Perform a step of the simulated annealing algorithm. """

    # save the old configuration
    old_config = copy.deepcopy(configuration.particles)

    for part1, part2 in configuration.pairs:
        print(part1.x, part1.y, part2.x, part2.y)


    # move a random particle
    configuration = mover(configuration)

    for part1, part2 in configuration.pairs:
        print(part1.x, part1.y, part2.x, part2.y)


    # calculate new score
    new_score = calc_score(configuration.pairs)

    # accept this move if the new score is lower, otherwise restore old configuration
    if new_score <= configuration.best_score:
        print("found new best score")
        configuration.best_score = new_score
        configuration.score = new_score
    else:
        difference = configuration.best_score - new_score
        acceptance_chance = math.exp(difference / configuration.current_temp)

        # accept it depending on the temperature
        if acceptance_chance < random.random():
            configuration.score = new_score
        else:
            configuration.particles = copy.deepcopy(old_config)

    return configuration




if __name__ == "__main__":
    main()