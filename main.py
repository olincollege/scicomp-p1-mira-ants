# from ant import Ant
from ant_simulation import Simulation

def main():
    sim = Simulation()
    # print(sim.array)
    # ant = Ant(sim)
    # print(ant.get_neighbors())
    # print(ant.choose_most_phermones_neighbor())

    # print(sim.array)
    sim.loop(100,print_iter=True,sleep=0.1)
    print(sim.array)
if __name__=="__main__":
    main()