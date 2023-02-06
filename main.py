from ant import Ant
from simulation import Simulation

def main():
    sim = Simulation((10,10))
    # print(space.array)
    # ant = Ant(space)
    # print(ant.get_neighbors())
    # print(ant.choose_most_phermones_neighbor())

    print(sim.array)
    sim.loop(10)
    print(sim.array)
if __name__=="__main__":
    main()