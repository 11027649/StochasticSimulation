import numpy as np
import matplotlib.pyplot as plt

def main():
    
    #of je seed wil
    #np.random.seed(1)
    
    #samples
    n = 10
    
    points = latin_hypercube(n)

    plotter(points, n, "own")

    #nlatin(N)

def orthogonal(n):
    """orthogonal sampling for n samples"""
    
    low_lim = np.arange(0, n)/n
    up_lim = np.arange(1, n+1)/n

def latin_hypercube(n):
    """Latin hypercube sampling for n samples"""

    low_lim = np.arange(0, n)/n
    up_lim = np.arange(1, n+1)/n

    #random points on grid
    points = np.random.uniform(low=low_lim, high = up_lim, size=[2,n]).T

    np.random.shuffle(points[:,1])

    print("LHS:")
    print(points)

    return points

def nlatin(N):
    real_intervals = np.linspace(0, 1, N + 1)
    im_intervals = np.linspace(0, 1, N + 1)

    # draw a list of tuples of coordinates, then shuffle
    points = np.empty(shape=(N, 2))

    for i in range(N):
        points[i, 0] = np.random.uniform(real_intervals[i], real_intervals[i + 1])
        points[i, 1] = np.random.uniform(im_intervals[i], im_intervals[i + 1])

    # shuffle y (im) coordinates
    np.random.shuffle(points[:, 1])

    print("N LHS:")
    print(points)

    return points

def plotter(p, n, title):
    plt.figure(figsize=[5,5])

    plt.title(title)
    plt.xlim([0,1])
    plt.ylim([0,1])
    plt.scatter(p[:,0], p[:,1])
    plt.axvline(x = 0.5, linewidth=4, color='r')
    plt.axhline(y = 0.5, linewidth=4, color='r')
    plt.xlabel("LHS: 1 punt per gridline, maar verschillend aantal punten per subvak")

    #create visual grid
    for i in np.arange(0, 1, 1/n):
        plt.axvline(i)
        plt.axhline(i)
    plt.show()


if __name__ == '__main__':
    main()