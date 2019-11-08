from numba import jit
import random
import csv
import numpy as np
import time

import math
import matplotlib.pyplot as plt

def main():

    # for each point we do 100 iterations to calculate whether it is in the set or not
    max_iters = 2000

    # coordinates
    real_min, real_max = -1, 2
    im_min, im_max = -1.25, 1.25

    # amount of points for integration (it must be able to be squared)
    N = 9

    # sanity check
    assert math.sqrt(N) == math.floor(math.sqrt(N)), "must be able to be squared"

    # define N intervals in both real and imaginary direction
    real_intervals = np.linspace(real_min, real_max, N + 1)
    im_intervals = np.linspace(im_min, im_max, N + 1)

    total_area = (abs(real_min) + abs(real_max)) * (abs(im_min) + abs(im_max))

    generate_o(real_min, real_max, im_min, im_max, N)
    # area = orthogonal_integration(real_intervals, im_intervals, max_iters, total_area, N)

    # with open("../results/orthogonal_integration_results.csv", 'a') as resultsfile:
    #     writer = csv.writer(resultsfile, delimiter=',')
    #     writer.writerow([max_iters, N, area])


@jit(nopython=True)
def orthogonal_integration(real_intervals, im_intervals, maxiter, total_area, N):
    """ Calculates the area of the Mandelbrot Set using 2D latin cube integration.
        Does this using N points. Latin cube sampling spreads the sample points
        'more uniformly' across all of the possible values than the basic MC method.
        In theory we found that the area has to be somewhere around
        sqrt(6*pi - 1) - e = 1.506591... (see report for details) """

    total_points = 9
    subgrids_per_axis = 3
    subgrids = subgrids_per_axis * subgrids_per_axis
    subpoints = total_points /  subgrids_per_axis

    points_in_set = 0

    # draw a list of tuples of coordinates, then shuffle
    points = np.empty(shape=(N, 2))

    subgrid_nr = 0

    start_real = subgrid_nr * subpoints
    end_real = start_real + subpoints + 1

    for i in range(subgrids):
        print("Subgrid nummer: ", subgrid_nr)

        start_im = subgrid_nr %  subgrids_per_axis * subpoints # 2 klopt niet als het om meer subgrids gaat
        end_im = start_im + subpoints + 1 # also include the last point/boundary

        im_subgrid_range = im_intervals[start_im:end_im]
        real_subgrid_range = real_intervals[start_real:end_real]

        print("real (x): ", real_subgrid_range, len(real_subgrid_range))
        print("im (y): ", im_subgrid_range, len(im_subgrid_range))

        for i in range(subpoints):
            points[i, 0] = np.random.uniform(real_intervals[i], real_intervals[i + 1])
            points[i, 1] = np.random.uniform(im_intervals[i], im_intervals[i + 1])

        # shuffle y (im) coordinates
        np.random.shuffle(points[:, 1])

        # move to next subgrid
        subgrid_nr += 1

        if subgrid_nr %  subgrids_per_axis == 0:
            start_real = start_real + subpoints
            end_real = start_real + subpoints + 1


    # loop over each point in the plane and count the number of points in the set
    for n in range(N):
        c = complex(points[n, 0], points[n , 1])

        if in_mandelbrot(c, maxiter):
            points_in_set += 1

    return float(points_in_set) * total_area / total_points


def generate_o(real_min, real_max, im_min, im_max, samples):

    values_i = []
    values_r = []

    subgrids = int(math.sqrt(samples))

    scale_im = (im_max - im_min) / samples
    scale_real = (real_max - real_min) / samples;

    xlist = [[0 for i in range(subgrids)] for j in range(subgrids)]
    ylist = [[0 for i in range(subgrids)] for j in range(subgrids)]

    for row in xlist:
        print(row)

    m = 0

    for i in range(subgrids):
        for j in range(subgrids):
            xlist[i][j] = ylist[i][j] = m
            m += 1


    np.random.shuffle(xlist)
    np.random.shuffle(ylist)


    for row in xlist:
        print(row)

    for i in range(subgrids):
        for j in range(subgrids):
            values_i.append(im_min + scale_im * (xlist[i][j] + np.random.random() ))
            values_r.append(real_min + scale_real * (ylist[j][i] + np.random.random() ))

    for i in range(len(values_i)):
        print(values_i[i], values_r[i])

    plt.xlim((real_min, real_max))
    plt.ylim((im_min, im_max))
    plt.ylabel("Imaginary")
    plt.xlabel("Real")

    plt.scatter(values_r, values_i)

    for i in range(9):

        plt.hlines(im_min + i * scale_im, real_min, real_max)
        plt.vlines(real_min + i * scale_real, im_min, im_max)

    plt.savefig("test")



    return values_i, values_r


@jit(nopython=True)
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
