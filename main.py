# from ant import Ant
from ant_simulation import Simulation
import matplotlib.pyplot as plt

def main():
    # sim = Simulation(shape=(11,11))
    sim = Simulation(shape=(101,101))
    # print(sim.array)
    # ant = Ant(sim)
    # print(ant.get_neighbors())
    # print(ant.choose_most_phermones_neighbor())

    # print(sim.array)
    # sim.loop(100,print_iter=True)
    # sim.loop(50)
    sim.loop(100)
    print(sim.array)
    sim.draw()
    # plt.show()
if __name__=="__main__":
    main()