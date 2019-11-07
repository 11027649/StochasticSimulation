from numba import jit
import random
import csv
import numpy as np
import time

def main():

    # for each point we do 100 iterations to calculate whether it is in the set or not
    max_iters = 1000

    # coordinates
    real_min, real_max = -2, 1
    im_min, im_max = -1.25, 1.25

    # amount of points for integration
    total_points = np.arange(1000, 100000, 1000)

    for points in total_points:
        print("points: ", points)

        for test in range(1000):
            starttime = time.time()

            N = points

            # define N intervals in both real and imaginary direction
            real_intervals = np.linspace(real_min, real_max, N + 1)
            im_intervals = np.linspace(im_min, im_max, N + 1)

            total_area = (abs(real_min) + abs(real_max)) * (abs(im_min) + abs(im_max))

            area = orthogonal_integration(real_intervals, im_intervals, max_iters, total_area, points)

            endtime = time.time()

            with open("results/latin_cube_integration_results.csv", 'a') as resultsfile:
                writer = csv.writer(resultsfile, delimiter=',')
                writer.writerow([max_iters, points, area, endtime - starttime])


@jit(nopython=True, parallel=True)
def orthogonal_integration(real_intervals, im_intervals, maxiter, total_area, N):
    """ Calculates the area of the Mandelbrot Set using 2D latin cube integration.
        Does this using N points. Latin cube sampling spreads the sample points
        'more uniformly' across all of the possible values than the basic MC method.
        In theory we found that the area has to be somewhere around
        sqrt(6*pi - 1) - e = 1.506591... (see report for details) """

    total_points = N
    subgrids = 2 * 2
    subpoints = total_points / (subgrids / 2)

    points_in_set = 0

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

        if in_mandelbrot(c, maxiter):
            points_in_set += 1

    return float(points_in_set) * total_area / total_points



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
