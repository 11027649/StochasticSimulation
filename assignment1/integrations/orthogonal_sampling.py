from numba import jit
import random
import csv
import numpy as np
import time
import matplotlib.pyplot as plt
import math

from helpers import generate_orthogonal, hit_miss_mc

def main():

    # for each point we do 100 iterations to calculate whether it is in the set or not
    maxiter = 2000

    # coordinates
    real_min, real_max = -2, 1
    im_min, im_max = -1.25, 1.25

    total_area = (abs(real_min) + abs(real_max)) * (abs(im_min) + abs(im_max))

    # amount of points for integration
    subgrid = 100
    total_points = 10000

    # do this 5000 times
    for trial in range(2500):
        starttime = time.time()

        orthogonal_complex_numbers = generate_orthogonal(real_min, real_max, im_min, im_max, subgrid, total_points)
        area = hit_miss_mc(orthogonal_complex_numbers, maxiter, total_points, total_area)

        endtime = time.time()

        with open("../data/orthogonal_integration.csv", 'a') as resultsfile:
            writer = csv.writer(resultsfile, delimiter=',')
            writer.writerow([maxiter, total_points, area, endtime - starttime])


if __name__ == '__main__':
    main()
