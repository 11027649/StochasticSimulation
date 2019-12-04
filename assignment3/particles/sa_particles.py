from helpers import Particle, Optimize_Charge

def main():
    algorithm = Optimize_Charge(amount_of_particles=12, radius=1)
    algorithm.visualize()


if __name__ == "__main__":
    main()