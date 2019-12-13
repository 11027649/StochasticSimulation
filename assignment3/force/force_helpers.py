import random
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from itertools import combinations
import copy
import pickle

from Particle import Particle

class Optimize_Charge():
    def __init__(self, amount_of_particles, radius):
        self.radius = radius
        self.particles = self.initialize(amount_of_particles)
        self.score = self.calc_score()

    def initialize(self, amount_of_particles):
        particles = []

        for i in range(amount_of_particles):
            # get a random angle
            angle = random.uniform(0, 360)

            # get a random distance < radius
            distance = random.uniform(0, self.radius)

            # calculate x and y coordinates

            particle = Particle(id = i, coordx= distance*math.cos(angle), coordy=distance*math.sin(angle))
            particles.append(particle)

        return particles


    def visualize(self, title):
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
        for particle in self.particles:
            plt.scatter(particle.x, particle.y)

        fig.savefig(title)

    def calc_score(self):
        """ Uses the formula as defined in the assignment to calculate the charge of the current
            configuration of the particles."""

        # turn particles into pairs to avoid double counting
        pairs = list(grouper(self.particles))

        # minimize this
        E_pot = 0

        for part1,part2 in pairs:
            dist = self.inter_particle_distance(part1, part2)

            E_pot += 1/dist

        # score based on the total amount of potential energy (minimum is optimal)
        return E_pot

    def inter_particle_distance(self, part1, part2):
        """ Calculates the distance between two particles using Pythagoras. """

        return math.sqrt((part1.x - part2.x)**2 + (part1.y - part2.y)**2)

    def function(self):
        positions = np.zeros((len(self.particles),2))

        counter = 0
        for particle in self.particles:
            x, y = particle.x, particle.y
            positions[counter][0] = x
            positions[counter][1] = y
            counter += 1

        differences = np.zeros((positions.shape[0], positions.shape[0],2))

        counter = 0
        for i in positions:
            differences[counter] = i - positions
            counter += 1

        norm = np.sum(np.abs(differences**2),axis=-2)**(3/2)

        forces = differences/norm

        net_forces = np.array([sum(i) for i in forces])

        return positions, net_forces


    def move_all(self):
        positions, net_forces = self.function()

        new_pos = positions + 0.01*net_forces

        counter = 0
        for particle in self.particles:
            if not math.sqrt((new_pos[counter][0])**2 + (new_pos[counter][1])**2) > self.radius:
                particle.x = new_pos[counter][0]
                particle.y = new_pos[counter][1]
            counter += 1


    def simannealing_step(self, cooling_per_step):
        """ Perform a step of the simulated annealing algorithm. """

        # save the old configuration
        old_config = copy.deepcopy(self.particles)


        self.move_all()

        # calculate new score
        new_score = self.calc_score()

        # accept this move if the new score is lower, otherwise restore old configuration
        if new_score <= self.score:
            self.score = new_score
        else:
            difference = self.score - new_score
            acceptance_chance = math.exp(difference / self.current_temp)

            # accept it depending on the temperature
            if acceptance_chance < random.random():
                self.score = new_score
            else:
                self.particles = copy.deepcopy(old_config)

        self.current_temp -= cooling_per_step


    def run_sa(self, steps):
        self.scores_list = []
        self.max_temperature = 100
        self.min_temperature = 1
        self.current_temp = 100

        cooling_per_step = (self.max_temperature - self.min_temperature)/steps
        self.step = 0
        for self.step in range(steps):
            self.simannealing_step(cooling_per_step)
            self.scores_list.append(self.score)



def grouper(groupset):
    pairs = list(combinations(groupset, 2))
    return(pairs)
