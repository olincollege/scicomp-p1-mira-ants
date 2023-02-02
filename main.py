import ant
import space

def main():
    this_space = space.Space([5,5])
    print(this_space.space)
    this_ant = ant.Ant(this_space)
    print(this_ant.get_neighbors())
    print(this_ant.choose_most_phermones_neighbor())

if __name__=="__main__":
    main()