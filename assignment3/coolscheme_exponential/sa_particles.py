from Optimize import Optimize_Charge
import matplotlib.pyplot as plt
import os
import math
import pickle
import sys

from helpers import visualize

def main():
    if not len(sys.argv) == 2:
        print("usage: python sa_particles.py <no of particles>")
        sys.exit(1)


     # pick between "exponential", "linear", "reheat"
    coolscheme = "reheat"

    amount_of_particles = int(sys.argv[1])
    algorithm = Optimize_Charge(amount_of_particles, radius=1)

    algorithm.calc_score()

    max_iter = 100
    algorithm.run_sa(steps = max_iter, coolscheme=coolscheme)

    # save_best(algorithm, amount_of_particles)



def save_best(algorithm, amount_of_particles):
    # sanity checks for result folders
    if not os.path.exists("results"):
        os.makedirs("results")

    resultsDir = "results/" + str(amount_of_particles) + "_particles/"

    if not os.path.exists(resultsDir):
        os.makedirs(resultsDir)

    # save best results
    old_score = None
    old_file = None

    for file in os.listdir(resultsDir):
        if file.startswith("score"):
            old_score = float(file.split("#")[1])
            old_file = file
    if not old_score:
        old_score = math.inf

    if algorithm.score < old_score:
        if old_file:
            os.remove(resultsDir + old_file)
        with open(resultsDir + "score#" + str(algorithm.score) + "#.pickle", "wb") as handle:
            pickle.dump(algorithm, handle)

        visualize(title=resultsDir + "best_configuration.png", particles=algorithm.particles)
        plt.figure()
        plt.plot(range(len(algorithm.scores_list)), algorithm.scores_list)
        plt.savefig("sa.png")

    # save all scores
    with open(resultsDir + "results.txt", 'a') as resultsFile:
        resultsFile.write(str(algorithm.score) + "\n")



if __name__ == "__main__":
    main()