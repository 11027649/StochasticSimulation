# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This program is made to investigate the Mandelbrot Set. This is done by
# calculating and plotting the plane of numbers for which the Mandelbrot
# function does not converge. It is the first part of the first assignment for
# the Stochastic Simulation course on the UvA in the master Computational Science.
#
# Tristan Assenmacher and Natasja Wezel
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import matplotlib.pyplot as plt
from numba import jit
import numpy as np
import random
import time
import os

def main():

    # for each point we do 80 iterations to calculate whether it is in the set or not
    max_iterations = 80

    # coordinates
    # real_min, real_max = -1.25, 1.25
    real_min, real_max = -2, 1
    im_min, im_max = -1.25, 1.25

    # discretization steps
    width, height = 10000, 10000

    # calculate and plot the mandelbrot set
    plane = mandelbrot_set(real_min, real_max, im_min, im_max, width, height, max_iterations)
    plot_mandelbrot(plane)

    # amount of points for integration
    total_points = 10**6

    mandelbrot_area_mc(real_min, real_max, im_min, im_max, total_points)
    mandelbrot_area_latin_cube(real_min, real_max, im_min, im_max, total_points)

def plot_mandelbrot(plane):
    """ Plots the set. """

    # TODO: fix the x/y ticks (from -2,1 and from -1 to 1)
    plt.imshow(plane.T, origin='lower')
    plt.ylabel("Im")
    plt.xlabel("Re")

    if not os.path.isdir("figures"):
        os.makedirs("figures")

    plt.savefig("figures/mandelbrot_" + str(time.time()) + ".png")

@jit
def not_in_mandelbrot(c, maxiter=1000):
    """ Calculates whether a given complex number (c) is in the Mandelbrot Set
        or not. """

    z = 0 + 0j

    for n in range(maxiter):

        # if abs(z) > 2, it is in the set
        if abs(z) > 2:
            return n

        # update z using the Mandelbrot formula.
        z = z * z + c

    # if not in the set, return True
    return False

@jit
def is_in_circle(c, maxiter=100):
    """ calculates whether a given complex number (c) is in the Circle or not.
        For testing purposes. """

    if abs(c) < 1:
        return True

    return False

@jit
def mandelbrot_set(real_min, real_max, im_min, im_max, width, height, maxiter):
    """ For each point on a given grid, calculates whether it belongs to the
        Mandelbrot set or not. """

    # define axis and plane
    real_axis = np.linspace(real_min, real_max, width)
    im_axis = np.linspace(im_min, im_max, height)
    plane = np.empty((width,height))

    # loop over each point in the plane and call the mandelbrot() function
    for i in range(width):
        for j in range(height):
            plane[i,j] = not_in_mandelbrot(real_axis[i] + 1j * im_axis[j], maxiter)

    return plane

@jit
def mandelbrot_area_mc(real_min, real_max, im_min, im_max, N):
    """ Calculates the area of the Mandelbrot Set using Monte Carlo integration.
        Does this using N points. In theory we found that the area has to be
        somewhere around sqrt(6*pi - 1) - e = 1.506591... (see report for details) """

    total_points = N
    points_in_set = 0

    # loop over each point in the plane and count the number of points in the set
    for n in range(N):
        c = complex(random.uniform(real_min, real_max), random.uniform(im_min, im_max))
        # test = is_in_mandelbrot(c)

        if not not_in_mandelbrot(c):
            # print(n)
            points_in_set += 1


    total_area = (abs(real_min) + abs(real_max)) * (abs(im_min) + abs(im_max))

    print("\nMC integration")
    print("points in set:", points_in_set, "\ntotal points: ", total_points, "\narea: ", points_in_set * total_area/ total_points, "\n")

    return float(points_in_set) * total_area / total_points

@jit
def mandelbrot_area_latin_cube(real_min, real_max, im_min, im_max, N):
    """ Calculates the area of the Mandelbrot Set using 2D latin cube integration.
        Does this using N points. Latin cube sampling spreads the sample points
        'more uniformly' across all of the possible values than the basic MC method.
        In theory we found that the area has to be somewhere around
        sqrt(6*pi - 1) - e = 1.506591... (see report for details) """

    total_points = N
    points_in_set = 0

    # define N intervals in both real and imaginary direction
    real_intervals = np.linspace(real_min, real_max, N + 1)
    im_intervals = np.linspace(im_min, im_max, N + 1)

    # draw a list of tuples of coordinates, then shuffle
    points = np.empty(shape=(N, 2))

    for i in range(N):
        points[i, 0] = np.random.uniform(real_intervals[i], real_intervals[i + 1])
        points[i, 1] = np.random.uniform(im_intervals[i], im_intervals[i + 1])

    # shuffle y (im) coordinates
    np.random.shuffle(points[:, 1])

    # loop over each point in the plane and count the number of points in the set
    for n in range(N):
        c = complex(points[n, 0], points[n , 1])

        if not not_in_mandelbrot(c):
            points_in_set += 1

    total_area = (abs(real_min) + abs(real_max)) * (abs(im_min) + abs(im_max))

    print("2D Latin Cube integration")
    print("points in set:", points_in_set, "\ntotal points: ", total_points, "\narea: ", points_in_set * total_area/ total_points, "\n")


    return float(points_in_set) * 6 / total_points, total_points


if __name__ == '__main__':
    main()
