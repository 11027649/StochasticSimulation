import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from itertools import combinations

def visualize(title, particles):
    """ Visualizes the particles in the circle. """

    plt.figure(figsize=(10,10))
    plt.title("Best configuration for " + str(len(particles)) + " particles", size=25)
    plt.xlabel("xcoordinate", size=18)
    plt.ylabel("ycoordinate", size=18)

    plt.xticks(size=13)
    plt.yticks(size=13)

    circle = plt.Circle((0, 0), 1)
    circle.set_edgecolor("red")
    circle.set_facecolor("none")
    fig = plt.gcf()
    ax = fig.gca()

    ax.add_artist(circle)
    plt.xlim(-1.1,1.1)
    plt.ylim(-1.1,1.1)

    # draw all the particles
    for particle in particles:
        plt.scatter(particle.x, particle.y)

    fig.savefig(title)


def plot_convergence_and_temp(filename, algorithm):
    """ Plots the convergence of the score and the temperature. """

    plt.figure(figsize=(8, 8))
    plt.title("Convergence of score\n coolscheme:" + algorithm.coolscheme + ", " + str(len(algorithm.particles)) + " particles", size=25)

    # x axis
    plt.xticks(size=13)
    plt.xlabel("Steps", size=18)

    # left y axis
    ax1 = plt.gca()
    ax1.set_ylabel("Score (total reciprocal of distance)", size=18)
    label1 = ax1.plot(range(len(algorithm.scores_list)), algorithm.scores_list, color="turquoise", label="Score")
    plt.yticks(size=13)

    # right y axis
    ax2 = ax1.twinx()
    ax2.set_ylabel("Temperature", size=18)
    label2 = ax2.plot(range(len(algorithm.temperatures)), algorithm.temperatures, color="orchid", label="Temperature")
    plt.yticks(size=13)

    # labels en legend
    plots = label1 + label2
    labs = [l.get_label() for l in plots]
    legend = ax1.legend(plots, labs, loc='upper right')
    legend.FontSize = 20
    plt.savefig(filename)


def grouper(groupset):
    """ Returns a list of all possible combinations. """

    return list(combinations(groupset, 2))
