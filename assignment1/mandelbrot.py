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
    max_iterations_list = [100, 200, 500, 1000, 1500, 2000, 2500]
    max_iterations_list = [2000, 2500]
    # discretization steps
    width, height = 10000, 10000

    print("Starting now............")

    for max_iterations in max_iterations_list:
        print(max_iterations)

        # zoom coordinates
        # real_min, real_max = -0.7463, -0.7413
        # im_min, im_max = 0.1102, 0.1152

        # plane = mandelbrot_set(real_min, real_max, im_min, im_max, width, height, max_iterations)
        # calculate and plot the mandelbrot set
        # plot_mandelbrot(plane, max_iterations)

        real_min, real_max = -0.74877, -0.74872
        im_min, im_max = 0.065053, 0.065103
        plane = mandelbrot_set(real_min, real_max, im_min, im_max, width, height, max_iterations)
        plot_mandelbrot(plane, max_iterations)

        # normal coordinates
        # real_min, real_max = -2, 1
        # im_min, im_max = -1.25, 1.25
        # plane = mandelbrot_set(real_min, real_max, im_min, im_max, width, height, max_iterations)
        # plot_mandelbrot(plane, max_iterations)


def plot_mandelbrot(plane, iters):
    """ Plots the set. """

    colormaps = [plt.cm.magma, plt.cm.twilight, plt.cm.hot]

    for colormap in colormaps:
        plt.figure()

        # TODO: fix the x/y ticks (from -2,1 and from -1 to 1)
        colormap.set_under(color='black')
        plt.imshow(plane.T, origin='lower', cmap=colormap, vmin=0.0001, interpolation='bicubic')
        plt.ylabel("Im")
        plt.xlabel("Re")
        plt.title("cmap:" + str(colormap.name) + "\niters: " + str(iters))

        if not os.path.isdir("figures"):
            os.makedirs("figures")

        try:
            plt.savefig("figures/mandelbrot_" + str(time.time()) + ".png")
        except ValueError:
            print("Everything is 0?", iters)

        plt.close()

@jit(nopython=True)
def not_in_mandelbrot(c, maxiter):
    """ Calculates whether a given complex number (c) is in the Mandelbrot Set
        or not. """

    real = c.real
    imag = c.imag

    for n in range(maxiter):
        real2 = real * real
        imag2 = imag * imag

        # if abs(z) > 2, it is in the set: this is computationally expensive tho
        if real2 + imag2 > 4.0:
            return n

        # update z using the Mandelbrot formula.
        imag = 2 * real * imag + c.imag
        real = real2 - imag2 + c.real

    # if not in the set, return False
    return False


@jit(nopython=True, parallel=True)
def mandelbrot_set(real_min, real_max, im_min, im_max, width, height, maxiter):
    """ For each point on a given grid, calculates whether it belongs to the
        Mandelbrot set or not. """

    # define axis and plane
    real_axis = np.linspace(real_min, real_max, width)
    im_axis = np.linspace(im_min, im_max, height)
    plane = np.empty((width,height))

    # loop over each point in the plane and call the mandelbrot() function
    for i in range(width):
        if i%100 ==0:
            print("progres: ", i, "/", width)

        for j in range(height):
            plane[i,j] = not_in_mandelbrot(real_axis[i] + 1j * im_axis[j], maxiter)

    return plane

if __name__ == '__main__':
    main()
