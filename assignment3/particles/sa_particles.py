from helpers import Particle, Optimize_Charge
import matplotlib.pyplot as plt


def main():
    algorithm = Optimize_Charge(amount_of_particles=12, radius=1)

    algorithm.visualize("initialized.png")

    algorithm.calc_score()

    max_iter = 10000
    algorithm.run_sa(steps = max_iter)

    plt.figure()
    plt.plot(range(max_iter), algorithm.scores_list)
    plt.title("best score: ")
    plt.savefig("scores.png")

    algorithm.visualize("final_config.png")



if __name__ == "__main__":
    main()