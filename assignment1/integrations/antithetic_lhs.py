from numba import jit
import random
import csv
import numpy as np
import time

from helpers import generate_lh, generate_orthogonal, hit_miss_mc

def main():

    # for each point we do 100 iterations to calculate whether it is in the set or not
    maxiter = 2000

    # coordinates
    real_min, real_max = -2, 1
    im_min, im_max = -1.25, 1.25

    # amount of points for integration
    total_points = 10000

    total_area = (abs(real_min) + abs(real_max)) * (abs(im_min) + abs(im_max))

    # define N intervals in both real and imaginary direction
    real_intervals = np.linspace(real_min, real_max, total_points + 1)
    im_intervals = np.linspace(im_min, im_max, total_points + 1)

    iters = [100, 500, 1000, 1500, 2500, 3000]

    for maxiter in iters:
        for test in range(2500):
            starttime = time.time()

            points1 = generate_lh(real_intervals, im_intervals, total_points)
            area_x1 = hit_miss_mc(points1, maxiter, total_points, total_area)

            # create antithetic variate points
            points2 = [complex(-0.5-(c.real + 0.5), -1*c.imag) for c in points1]
            area_x2 = hit_miss_mc(points2, maxiter, total_points, total_area)

            endtime = time.time()

            print(test, area_x1, area_x2)

            with open("../data/antithetic_latin_hypercube_2000_100.csv", 'a') as resultsfile:
                writer = csv.writer(resultsfile, delimiter=',')
                writer.writerow([maxiter, total_points, area_x1, area_x2, endtime - starttime])


if __name__ == '__main__':
    main()
