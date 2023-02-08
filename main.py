# from ant import Ant
from ant_simulation import Simulation
import matplotlib.pyplot as plt
import numpy as np

def main():
    # sim = Simulation(shape=(11,11))
    # np.random.seed(69)
    sim = Simulation(shape=(101,101), phermone_deposit_rate = 5, fidelity_min = 0.1, fidelity_max = 0.9, phermone_max = 20, trail_level = 3)
    # print(sim.array)
    # ant = Ant(sim)
    # print(ant.get_neighbors())
    # print(ant.choose_most_phermones_neighbor())

    # print(sim.array)
    # sim.loop(2,print_iter=True)
    sim.loop(20)
    sim.draw()
    plt.figure()
    sim.loop(80)
    sim.draw()
    plt.figure()
    sim.loop(400)
    sim.draw()
    plt.figure()
    sim.loop(2500)
    sim.draw()
    plt.show()
    sim.loop(7000)
    sim.draw()
    plt.show()

    # sim.loop(10000)
    # sim.draw()
    # plt.show()
if __name__=="__main__":
    main()