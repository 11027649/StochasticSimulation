import numpy as np
import matplotlib.pyplot as plt
import math
import random
import copy

class City():
    def __init__(self, id, coord_x, coord_y):
        self.id = id
        self.x = coord_x
        self.y = coord_y
        self.connection = None

    def set_connection(self, id):
        self.connection = id

    def __str__(self):
        return f"city {self.id} with x: {self.x} and y: {self.y} and is connected to: {self.connection}"


class Optimize_TSP():
    def __init__(self, coordinate_file):
        self.cities = self.get_cities(coordinate_file)
        self.amount = len(self.cities)
        self.initialize()
        self.best_score = self.calc_score()


    def get_cities(self, coordinate_file):
        # read txt file with city information
        with open(coordinate_file, 'r') as cities_info:
            cities = cities_info.readlines()

        # create a dictionary to hold all city objects
        citylist = {}

        # fill dictionary with cities with their id as key
        for city in cities[6:-1]:
            id, x, y = city.strip().split()
            city = City(id=int(id) - 1, coord_x=int(x), coord_y=int(y))
            citylist[int(id) - 1] = city

        return citylist

    def initialize(self):
        """ Initializes a random path between all the cities. """

        # randomly initialize the connections between cities
        ids = np.arange(1, self.amount)
        np.random.shuffle(ids)

        # let city 0 point at first random id
        self.cities[0].set_connection(id=ids[0])

        # last city points at 0
        self.cities[ids[-1]].set_connection(id=0)


        # connect each city to another city in a "circle"
        for i in range(self.amount - 2):
            self.cities[ids[i]].set_connection(id=ids[i + 1])



    def change_connections(self):
        """ Randomly changes the connections of a cities. """

        city1_id = random.randint(0, self.amount - 1)
        city1 = self.cities[city1_id]

        city2_id = city1.connection
        city2 = self.cities[city2_id]

        city3_id = city2.connection
        city3 = self.cities[city3_id]

        # delete connection from city 1 and make a new one to city 3
        city1.set_connection(city3_id)

        # set other connection
        city2.set_connection(city3.connection)
        city3.set_connection(city2_id)


    def hillclimber_step(self):
        """ Changes connections of cities, calculates new score. Accepts if new score is lower,
            otherwise rolls back to old state. """

        old_cities = copy.copy(self.cities)

        self.change_connections()
        new_score = self.calc_score()

        if new_score < self.best_score:
            self.best_score = new_score
        else:
            self.cities = copy.copy(old_cities)

    def simannealing_step(self, cooling_per_step):
        """ Changes connections of cities, calculates new score. Accepts if new score is lower,
            otherwise whether it is accepted or not is based on the current temperature of the
            system. """

        old_cities = copy.copy(self.cities)

        self.change_connections()
        new_score = self.calc_score()

        if new_score < self.best_score:
            self.best_score = new_score
        else:
            difference = new_score - self.best_score
            acceptance_chance = math.exp(difference / self.current_temp)

            # accept it depending on the temperature


            if acceptance_chance < random.random():
                self.best_score = new_score
                print(acceptance_chance, "temp: ", self.current_temp, "accepted")
            else:
                print(acceptance_chance, "temp: ", self.current_temp, "rollback")
                self.cities = copy.copy(old_cities)

        self.current_temp -= cooling_per_step


    def run_sa(self, steps):
        self.scores_list = []
        self.max_temperature = 100
        self.current_temp = 100

        cooling_per_step = self.max_temperature/steps

        for step in range(steps):
            if step % 1000 == 0:
                print(step, self.best_score, self.current_temp)

            self.simannealing_step(cooling_per_step)
            self.scores_list.append(self.best_score)



    def run_hillclimber(self, steps):
        self.scores_list = []

        for step in range(steps):
            if step % 1000 == 0:
                print(step, self.best_score)
            self.hillclimber_step()
            self.scores_list.append(self.best_score)


    def visualize(self, filename):
        """ Visualizes the cities on its coordinates and the current path between
            the cities. """

        plt.figure()

        for id in self.cities:
            city = self.cities[id]

            # draw the city
            plt.scatter(city.x, city.y)
            # draw it's path to the next city
            plt.plot([self.cities[city.connection].x, city.x],
                        [self.cities[city.connection].y, city.y])

        plt.savefig(filename)


    def calc_score(self):
        """ Calculates the distance of the current path between cities.
            This distance is also the score. """

        distance = 0

        for id in self.cities:
            city = self.cities[id]

            # calculate the distance between this city and the city it is connected to
            dist = math.sqrt((abs(city.x - self.cities[city.connection].x))**2 +
                                (abs(city.y - self.cities[city.connection].y))**2)

            distance += dist

        return distance

    def print_cities(self):
        for city in self.cities.values():
            print(city)
