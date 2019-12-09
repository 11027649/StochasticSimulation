import random
import numpy as np
from numba import jit

def generate_random(real_min, real_max, im_min, im_max, N):
    """ Generates a list of N random complex numbers. """

    return [complex(random.uniform(real_min, real_max), random.uniform(im_min, im_max)) for n in range(N)]


def generate_lh(real_intervals, im_intervals, N):
    """ Generate a list of N complex numbers, sampled via the latin hypercube method. """

    # draw a list of tuples of coordinates, then shuffle
    points = np.empty(shape=(N, 2))

    for i in range(N):
        points[i, 0] = np.random.uniform(real_intervals[i], real_intervals[i + 1])
        points[i, 1] = np.random.uniform(im_intervals[i], im_intervals[i + 1])

    # shuffle y (im) coordinates
    np.random.shuffle(points[:, 1])

    return [complex(points[n, 0], points[n , 1]) for n in range(len(points))]


def generate_orthogonal(real_min, real_max, im_min, im_max, subgrids, N):
    """ Generates a list of N orthogonally sampled complex numbers. """

    # empty lists to contain both parts of the complex numbers
    values_i = []
    values_r = []

    # scale of the axes
    scale_im = (im_max - im_min) / N
    scale_real = (real_max - real_min) / N;

    # create empty 2D arrays for orthogonal points generation
    xlist = [[0 for i in range(subgrids)] for j in range(subgrids)]
    ylist = [[0 for i in range(subgrids)] for j in range(subgrids)]

    m = 0

    # fill arrays
    for i in range(subgrids):
        for j in range(subgrids):
            xlist[i][j] = m
            ylist[i][j] = m

            m += 1

    # shuffle the arrays
    np.random.shuffle(xlist)
    np.random.shuffle(ylist)

    # at each point in the array, put a random scaled value so that each row is mutually exclusive
    for i in range(subgrids):
        for j in range(subgrids):
            values_i.append(im_min + scale_im * (xlist[i][j] + np.random.random()))
            values_r.append(real_min + scale_real * (ylist[j][i] + np.random.random()))

    return [complex(values_r[i], values_i[i]) for i in range(len(values_r))]


@jit(nopython=True)
def hit_miss_mc(complexnumbers, maxiter, total_points, total_area):
    """ Calculates the area of the Mandelbrot Set using Monte Carlo integration.
        Does this using N points. In theory we found that the area has to be
        somewhere around sqrt(6*pi - 1) - e = 1.506591... (see report for details) """

    points_in_set = 0

    # loop over each point in the plane and count the number of points in the set
    for c in complexnumbers:

        if in_mandelbrot(c, maxiter):
            points_in_set += 1

    return points_in_set * total_area / total_points


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

    # if in the set, return True
    return True