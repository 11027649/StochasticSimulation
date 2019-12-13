from Optimize import Optimize_Charge
import matplotlib.pyplot as plt
import os
import math
import pickle
import sys

from helpers import visualize, plot_convergence_and_temp

def main():
    if not len(sys.argv) == 4:
        print("usage: python sa_particles.py <no of particles> <coolscheme> <iterations>")
        sys.exit(1)

    amount_of_particles = int(sys.argv[1])
    coolscheme = sys.argv[2]
    max_iter = int(sys.argv[3])


    if not coolscheme in ["exponential", "exponential_fast", "linear", "reheat"]:
        print("pick one of \"exponential\", \"linear\", \"reheat\"", "exponential_fast")

    algorithm = Optimize_Charge(amount_of_particles, radius=1)

    algorithm.run_sa(steps = max_iter, coolscheme=coolscheme)

    save_best(algorithm, amount_of_particles)


def save_best(algorithm, amount_of_particles):
    resultsDir = "results/" + str(amount_of_particles) + "_particles/" + algorithm.coolscheme + "/"

    # check if path exists
    if not os.path.exists(resultsDir):
        os.makedirs(resultsDir)

    # save best results
    old_score = math.inf
    old_file = None

    for file in os.listdir(resultsDir):
        if file.startswith("score"):
            old_score = float(file.split("#")[1])
            old_file = file

    if algorithm.score < old_score:
        if old_file:
            os.remove(resultsDir + old_file)
        with open(resultsDir + "score#" + str(algorithm.bestscore) + "#.pickle", "wb") as handle:
            pickle.dump(algorithm, handle)

        visualize(title=resultsDir + "best2_configuration.png", particles=algorithm.bestconfig)
        plt.figure()

        filename = resultsDir + "/convergence.png"
        plot_convergence_and_temp(filename, algorithm)

    # save all scores
    with open(resultsDir + "results.txt", 'a') as resultsFile:
        resultsFile.write(str(algorithm.score) + "\n")



if __name__ == "__main__":
    main()