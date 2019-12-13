import random
import math

import copy
import pickle

from Particle import Particle
from helpers import grouper, calc_score

class ParticleGrid():
    def __init__(self, amount_of_particles, radius, coolscheme, steps):
        self.radius = radius

        self.particles = self.initialize(amount_of_particles)

        # turn particles into pairs to avoid double counting
        self.pairs = grouper(self.particles)

        self.steps = steps
        self.temperatures = self.init_temperatures(coolscheme, steps)

        self.score = calc_score(self.pairs)
        self.best_score = self.score

        self.scores_list = []


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


    def init_temperatures(self, coolscheme, steps):
        temperatures = []

        max_temperature = 100
        min_temperature = 1
        self.current_temp = 100

        # prepare a list with the temperatures
        if coolscheme == "linear":
            cooling_per_step = (max_temperature - min_temperature)/steps
            temperatures = [max_temperature - cooling_per_step * step for step in range(steps)]

        elif coolscheme == "exponential":
            temperatures = [max_temperature * math.exp(-0.001*x) for x in range(steps)]

        elif coolscheme == "reheat":

            # cool twice as fast and reheat halfway through the simulation
            cooling_per_step = (max_temperature - min_temperature)/(0.5 * steps)
            temperatures = [max_temperature - cooling_per_step * step for step in range(int(0.5*steps))]

            # second half same coolscheme
            temperatures.extend(temperatures)

        return temperatures

