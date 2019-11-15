from numba import jit
import random
import csv
import numpy as np
import time

from helpers import generate_lh, hit_miss_mc

def main():
    # coordinates
    real_min, real_max = -2, 1
    im_min, im_max = -1.25, 1.25

    # for points in total_points:
    total_points = 10000
    maxiters = 2000

    total_area = (abs(real_min) + abs(real_max)) * (abs(im_min) + abs(im_max))

    for test in range(2500):
        starttime = time.time()

        # define N intervals in both real and imaginary direction
        real_intervals = np.linspace(real_min, real_max, total_points + 1)
        im_intervals = np.linspace(im_min, im_max, total_points + 1)

        points = generate_lh(real_intervals, im_intervals, total_points)
        area = hit_miss_mc(points, maxiters, total_points, total_area)

        endtime = time.time()

        print(test, area)

        with open("../data/latin_hypercube.csv", 'a') as resultsfile:
            writer = csv.writer(resultsfile, delimiter=',')
            writer.writerow([maxiters, total_points, area, endtime - starttime])


if __name__ == '__main__':
    main()
