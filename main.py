from ant import Ant
from space import Space

def main():
    space = Space((10,10),n=10)
    # print(space.array)
    # ant = Ant(space)
    # print(ant.get_neighbors())
    # print(ant.choose_most_phermones_neighbor())

    print(space.array)
    space.step()
    print(space.array)

if __name__=="__main__":
    main()