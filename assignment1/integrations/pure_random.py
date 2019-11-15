from numba import jit
import random
import csv
import numpy as np
import time

from helpers import generate_random, hit_miss_mc

def main():

    # coordinates
    real_min, real_max = -2, 1
    im_min, im_max = -1.25, 1.25

    total_area = (abs(real_min) + abs(real_max)) * (abs(im_min) + abs(im_max))

    # for points in total_points:
    total_points = 10000

    maxiter = 2000

    for test in range(2500):
        starttime = time.time()

        points = generate_random(real_min, real_max, im_min, im_max, total_points)
        area = hit_miss_mc(points, maxiter, total_points, total_area)

        endtime = time.time()
        print(test, area)

        with open("../data/random.csv", 'a') as resultsfile:
            writer = csv.writer(resultsfile, delimiter=',')
            writer.writerow([maxiter, total_points, area, endtime - starttime])


@jit(nopython=True, parallel=True)
def mandelbrot_area_mc(real_min, real_max, im_min, im_max, maxiter, N):
    """ Calculates the area of the Mandelbrot Set using Monte Carlo integration.
        Does this using N points. In theory we found that the area has to be
        somewhere around sqrt(6*pi - 1) - e = 1.506591... (see report for details) """

    total_points = N
    points_in_set = 0

    # loop over each point in the plane and count the number of points in the set
    for n in range(N):
        c = complex(random.uniform(real_min, real_max), random.uniform(im_min, im_max))

        if in_mandelbrot(c, maxiter):
            points_in_set += 1

    total_area = (abs(real_min) + abs(real_max)) * (abs(im_min) + abs(im_max))

    return points_in_set * total_area / total_points



@jit(nopython=True, parallel=True)
def in_mandelbrot(c, maxiter):
    """ Calculates whether a given complex number (c) is in the Mandelbrot Set
        or not. """

    z = 0 + 0j

    for n in range(maxiter):

        # if abs(z) > 2, it is in the set
        if abs(z) > 2:
            return False

        # update z using the Mandelbrot formula.
        z = c + z * z

    # if not in the set, return False
    return True

if __name__ == '__main__':
    main()
