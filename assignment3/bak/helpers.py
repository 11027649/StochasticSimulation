import random
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from itertools import combinations
import copy
import pickle
import os

from Particle import Particle

from numba import jit

def force_field(pairs):
    """function that calculates the total force on a particle in x and y direction"""

    x_vec = 0
    y_vec = 0

    #force per pair
    for part1, part2 in pairs:

        x_dist = abs(part1.x - part2.x)
        y_dist = abs(part1.y - part2.y)
        angle = math.degrees(math.atan(y_dist/x_dist))
        dist = inter_particle_distance(part1,part2)

        force = dist/(abs(dist)**3)

        opp_angle = 90-angle
        opp_x = math.sin(math.radians(opp_angle))*force
        opp_y = math.cos(math.radians(opp_angle))*force


def mover(configuration):
    """"move particles around randomly for now"""

    # unlucky random particle moves a small distance
    unlucky = random.choice(configuration.particles)
    xmove = random.uniform(-0.01,0.01)
    ymove = random.uniform(-0.01,0.01)

    if not math.sqrt((unlucky.x + xmove)**2 + (unlucky.y + ymove)**2) > configuration.radius:
        unlucky.x += xmove
        unlucky.y += ymove

        print("move")

    configuration.pairs = grouper(configuration.particles)

    return configuration


def calc_score(pairs):
    """ Uses the formula as defined in the assignment to calculate the charge of the current
        configuration of the particles."""

    # minimize this
    E_pot = 0

    for part1,part2 in pairs:
        dist = inter_particle_distance(part1, part2)

        E_pot += 1/dist

    # score based on the total amount of potential energy (minimum is optimal)
    return E_pot

def visualize(title, particles):
    """ Visualizes the particles in the circle. """

    plt.figure(figsize=(5,5))
    circle = plt.Circle((0, 0), 1)
    circle.set_edgecolor("red")
    circle.set_facecolor("none")
    fig = plt.gcf()
    ax = fig.gca()

    ax.add_artist(circle)
    plt.xlim(-1,1)
    plt.ylim(-1,1)

    # draw all the particles
    for particle in particles:
        plt.scatter(particle.x, particle.y)

    fig.savefig(title)


def plot_convergence_and_temp(filename, algorithm, coolscheme):
    """ Plots the convergence of the score and the temperature. """

    plt.figure(figsize=(8, 8))
    plt.title("Convergence of score\n coolscheme:" + coolscheme + ", " + str(len(algorithm.particles)) + " particles", size=25)

    # x axis
    plt.xticks(size=13)
    plt.xlabel("Steps", size=18)

    # left y axis
    ax1 = plt.gca()
    ax1.set_ylabel("Score (total reciprocal of distance)", size=18)
    label1 = ax1.plot(range(len(algorithm.scores_list)), algorithm.scores_list, color="turquoise", label="Score")
    plt.yticks(size=13)

    # right y axis
    ax2 = ax1.twinx()
    ax2.set_ylabel("Temperature", size=18)
    label2 = ax2.plot(range(len(algorithm.temperatures)), algorithm.temperatures, color="orchid", label="Temperature")
    plt.yticks(size=13)

    # labels en legend
    plots = label1 + label2
    labs = [l.get_label() for l in plots]
    legend = ax1.legend(plots, labs, loc='upper right')
    legend.FontSize = 20
    plt.savefig(filename)


def save_best(algorithm, amount_of_particles):
    # sanity checks for result folders
    if not os.path.exists("results"):
        os.makedirs("results")

    resultsDir = "results/" + str(amount_of_particles) + "_particles/"

    if not os.path.exists(resultsDir):
        os.makedirs(resultsDir)

    # save best results
    old_score = None
    old_file = None

    for file in os.listdir(resultsDir):
        if file.startswith("score"):
            old_score = float(file.split("#")[1])
            old_file = file
    if not old_score:
        old_score = math.inf

    if algorithm.score < old_score:
        if old_file:
            os.remove(resultsDir + old_file)
        with open(resultsDir + "score#" + str(algorithm.score) + "#.pickle", "wb") as handle:
            pickle.dump(algorithm, handle)

        visualize(title=resultsDir + "best_configuration.png", particles=algorithm.particles)
        plt.figure()
        plt.plot(range(len(algorithm.scores_list)), algorithm.scores_list)
        plt.savefig("sa.png")

    # save all scores
    with open(resultsDir + "results.txt", 'a') as resultsFile:
        resultsFile.write(str(algorithm.score) + "\n")


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

