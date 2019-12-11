import random
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from itertools import combinations
import copy
import pickle

from Particle import Particle


def grouper(groupset):
    """ Returns a list of pairs with all possible combinations of particles. """

    return list(combinations(groupset, 2))


def calc_distances(particles, pairs):
    """ Uses the formula as defined in the assignment to calculate the charge of the current
        configuration of the particles."""

    distances = {}

    for part1, part2 in pairs:
        distance = inter_particle_distance(part1, part2)
        print(distance)
        print(part1.x, part1.y, part2.x, part2.y)
        distances[(part1,part2)] = 1/distance

    # score based on the total amount of potential energy (minimum is optimal)
    return distances


def add_potentials(distances):
    """ Adds all the distances between every unique pair of particles. """

    return sum(distances.values())


def update_distances(distances, moved_particle):
    """ Updates only the potential energies of the moved particle to save computational time. """


    for (part1, part2) in distances:

        # update only if the distance has changed
        if part1 == moved_particle or part2 == moved_particle:
            distance = inter_particle_distance(part1, part2)

            print('distance', distance)
            print(distances[(part1,part2)])
            print('1/distance', 1/distance)

            distances[(part1,part2)] = 1/distance

    # score based on the total amount of potential energy (minimum is optimal)
    return distances


def inter_particle_distance(particle1, particle2):
    """ Calculates the distance between two particles using Pythagoras. """

    return math.sqrt(abs(particle1.x - particle2.x)**2 + abs(particle1.y - particle2.y)**2)

