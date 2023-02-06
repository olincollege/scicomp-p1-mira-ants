# from ant import Ant
from ant_simulation import Simulation
import matplotlib.pyplot as plt
import numpy as np

def main():
    # sim = Simulation(shape=(11,11))
    # np.random.seed(69)
    sim = Simulation(shape=(101,101), phermone_deposit_rate = 3, fidelity_min = 1, fidelity_max = 40, trail_level = 6)
    # print(sim.array)
    # ant = Ant(sim)
    # print(ant.get_neighbors())
    # print(ant.choose_most_phermones_neighbor())

    # print(sim.array)
    # sim.loop(2,print_iter=True)
    # sim.loop(50)
    sim.loop(100)
    # print(sim.array)
    sim.draw()
    sim.loop(400)
    sim.draw()
    # plt.show()
if __name__=="__main__":
    main()