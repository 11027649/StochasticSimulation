import random
import math

import copy
import pickle

from Particle import Particle
from helpers import grouper

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


    def calc_score(self):
        """ Uses the formula as defined in the assignment to calculate the charge of the current
            configuration of the particles."""

        # turn particles into pairs to avoid double counting
        pairs = grouper(self.particles)

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

    def force_field(self):
        """function that calculates the total force on a particle in x and y direction"""

        pairs = list(grouper(self.particles))


        x_vec = 0
        y_vec = 0

        #force per pair
        for part1, part2 in pairs:

            x_dist = abs(part1.x - part2.x)
            y_dist = abs(part1.y - part2.y)
            angle = math.degrees(math.atan(y_dist/x_dist))
            dist = self.inter_particle_distance(part1,part2)

            force = dist/(abs(dist)**3)

            opp_angle = 90-angle
            opp_x = math.sin(math.radians(opp_angle))*force
            opp_y = math.cos(math.radians(opp_angle))*force

            print(opp_angle,opp_x,opp_y)



    def mover(self):
        """"move particles around randomly for now"""

        # unlucky random particle moves a small distance
        unlucky = random.choice(self.particles)
        xmove = random.uniform(-0.01,0.01)
        ymove = random.uniform(-0.01,0.01)

        if not math.sqrt((unlucky.x + xmove)**2 + (unlucky.y + ymove)**2) > self.radius:
            unlucky.x += xmove
            unlucky.y += ymove


    def simannealing_step(self):
        """ Perform a step of the simulated annealing algorithm. """

        # save the old configuration
        old_config = copy.deepcopy(self.particles)

        # move a random particle
        self.mover()

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




    def run_sa(self, steps, coolscheme):
        self.scores_list = []
        self.temperatures = []


        self.max_temperature = 100
        self.min_temperature = 1
        self.current_temp = 100

        # prepare a list with the temperatures
        if coolscheme == "linear":
            cooling_per_step = (self.max_temperature - self.min_temperature)/steps
            self.temperatures = [self.max_temperature - cooling_per_step * steps for step in range(steps)]

        elif coolscheme == "exponential":
            self.temperatures = [self.max_temperature * math.exp(-0.01*x) for x in range(steps)]

        elif coolscheme == "reheat":

            # cool twice as fast and reheat halfway through the simulation
            cooling_per_step = (self.max_temperature - self.min_temperature)/(0.5 * steps)
            self.temperatures = [self.max_temperature - cooling_per_step * step for step in range(int(0.5*steps))]

            # second half same coolscheme
            self.temperatures.extend(self.temperatures)

        self.step = 0

        # run the algorithm
        for self.step in range(steps):

            # perform a step
            self.simannealing_step()

            # save the current score
            self.scores_list.append(self.score)

            # cool the system
            self.current_temp = self.temperatures[self.step]