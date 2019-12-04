import random
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class Particle():
    def __init__(self, coordx, coordy):
        self.x = coordx
        self.y = coordy

    def __str__(self):
        return f"Hi I am a particle at ({self.x}, {self.y})"

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

            particle = Particle(coordx= distance*math.cos(angle), coordy=distance*math.sin(angle))
            print(particle)
            particles.append(particle)

        return particles


    def visualize(self):
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

        fig.savefig('plotcircles.png')


    def calc_score(self):
        """ Uses the formula as defined in the assignment to calculate the charge of the current
            configuration of the particles."""

        charge = 0

        for particle in self.particles:

            # calculate the distance between all other particles
            for other_particle in self.particles:
                if not other_particle == particle:
                    dist = math.sqrt((abs(particle.x - other_particle.x))**2 +
                                        (abs(particle.y - other_particle.y))**2)

                    print(dist)


        return 0