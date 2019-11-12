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

    # amount of points for integration
    subgrids = np.arange(30, 1000, 10)
    print(subgrids, subgrids * subgrids)

    for subgrid in subgrids:
        samples = subgrid * subgrid

        print("points: ", samples)

        # sanity check
        assert math.sqrt(samples) == math.floor(math.sqrt(samples)), "must be able to be squared"

        total_area = (abs(real_min) + abs(real_max)) * (abs(im_min) + abs(im_max))

        for test in range(5000):
            starttime = time.time()

            real_parts, im_parts = generate_o(real_min, real_max, im_min, im_max, subgrid, samples)
            area = orthogonal_integration(real_parts, im_parts, samples, max_iters, total_area)

            endtime = time.time()

            with open("../results/orthogonal_integration_results.csv", 'a') as resultsfile:
                writer = csv.writer(resultsfile, delimiter=',')
                writer.writerow([max_iters, samples, area, endtime-starttime])


def orthogonal_integration(real_parts, im_parts, samples, maxiter, total_area):
    """ Calculates the area of the Mandelbrot Set using 2D orthogonal sampling.
        Does this using N points. Orthogonal sampling spreads the sample points
        'more uniformly' across all of the possible values than the basic MC/LH method.
        In theory we found that the area has to be somewhere around
        sqrt(6*pi - 1) - e = 1.506591... (see report for details) """

    points_in_set = 0

    # loop over each point in the plane and count the number of points in the set
    for n in range(samples):
        c = complex(real_parts[n], im_parts[n])

        if in_mandelbrot(c, maxiter):
            points_in_set += 1

    return float(points_in_set) * total_area / samples


def generate_o(real_min, real_max, im_min, im_max, subgrids, samples):
    """ Generates the coordinates of the points using orthogonal sampling. """

    values_i = []
    values_r = []

    scale_im = (im_max - im_min) / samples
    scale_real = (real_max - real_min) / samples;

    xlist = [[0 for i in range(subgrids)] for j in range(subgrids)]
    ylist = [[0 for i in range(subgrids)] for j in range(subgrids)]

    m = 0

    for i in range(subgrids):
        for j in range(subgrids):
            xlist[i][j] = ylist[i][j] = m
            m += 1

    np.random.shuffle(xlist)
    np.random.shuffle(ylist)

    for i in range(subgrids):
        for j in range(subgrids):
            values_i.append(im_min + scale_im * (xlist[i][j] + np.random.random() ))
            values_r.append(real_min + scale_real * (ylist[j][i] + np.random.random() ))

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
