import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from itertools import combinations

def visualize(title, particles):
    """ Visualizes the particles in the circle. """

    plt.figure(figsize=(5,5))
    circle = plt.Circle((0, 0), 1)
    circle.set_edgecolor("red")
    circle.set_facecolor("none")
    fig = plt.gcf()
    ax = fig.gca()

    ax.add_artist(circle)
    plt.xlim(-1,1)
    plt.ylim(-1,1)

    # draw all the particles
    for particle in particles:
        plt.scatter(particle.x, particle.y)

    fig.savefig(title)



def grouper(groupset):
    """ Returns a list of all possible combinations. """

    return list(combinations(groupset, 2))
