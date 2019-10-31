import matplotlib.pyplot as plt
from numba import jit
import numpy as np

def main():
    max_iterations = 80
    xmin, xmax = -2, 0.75
    ymin, ymax = -1.25, 1.25
    width, height = 10000, 10000

    _, _, n3 = mandelbrot_set(xmin, xmax, ymin, ymax, width, height, max_iterations)

    plt.imshow(n3)
    plt.show()


@jit
def mandelbrot(c, maxiter):
    z = c
    for n in range(maxiter):
        if abs(z) > 2:
            return n
        z = z*z + c
    return 0

@jit
def mandelbrot_set(xmin, xmax, ymin, ymax, width, height, maxiter):

    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width,height))

    for i in range(width):
        for j in range(height):
            n3[i,j] = mandelbrot(r1[i] + 1j*r2[j],maxiter)

    return (r1,r2,n3)

if __name__ == '__main__':
    main()
