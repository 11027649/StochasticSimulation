import matplotlib.pyplot as plt
from helpers import Optimize_TSP

def main():
    # cities = get_cities("tsp_configurations/pcb442.tsp.txt")
    # cities = get_cities("tsp_configurations/a280.tsp.txt")

    algorithm = Optimize_TSP(coordinate_file="tsp_configurations/eil51.tsp.txt")

    algorithm.visualize("after_initialization.png")

    max_iters = 100000
    algorithm.run_sa(steps=max_iters)

    plt.figure()
    plt.plot(range(max_iters), algorithm.scores_list)
    plt.title("Hillclimber, best score: ")
    plt.savefig("scores.png")

    algorithm.visualize("after_hillclimber.png")



if __name__ == "__main__":
    main()