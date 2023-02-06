import numpy as np
from scipy.signal import convolve2d
import random
class Ant:
    """Initialize the ant
    sim is the simulation the ant is a part of (for calling simulation modifying functions)
    See ant_simulation for parameter definitions
    """
    def __init__(self, sim, fidelity_min, fidelity_max, phermone_max, trail_level):
        self.location = np.int_(np.round(np.divide(sim.array.shape,2)))
        self.following = False
        self.fidelity_min = fidelity_min
        self.fidelity_max = fidelity_max
        self.phermone_max = phermone_max
        self.sim = sim
        self.trail_level = trail_level

        # Directions that the ant can be pointing
        self.directions = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        # Directions Indices
        # 012
        # 7 3
        # 654

        # start in a random direction
        self.direction = np.random.randint(0,8)
        # self.direction = 5
        self.neighbor_kernel = np.ones((3,3))
        self.neighbor_kernel[1,1] = 0
        self.move_forward
        # print(self.neighbor_kernel)

    """Make a decision based on the local phermone count and the fidelity

    returns: boolean choice
    """
    def fidelity_test(self):
        pher_level = self.sim.array[*self.location]
        pher_frac = pher_level/self.phermone_max
        # print(self.sim.array)
        # print(pher_level)
        pher_frac = min(self.fidelity_max,pher_frac)
        pher_frac = max(self.fidelity_min,pher_frac)
        return (np.random.choice([True, False], p=[pher_frac,1-pher_frac]))

    """Get location of each neighbor

    returns: a list of 2-length tuples specifying neighbor locations
    """
    def get_neighbors(self):
        location_array = np.zeros_like(self.sim.array)
        # print(self.location)
        location_array[*self.location] = 1
        neighbors = convolve2d(location_array, self.neighbor_kernel, mode='same').nonzero()
        return list(zip(neighbors[0],neighbors[1]))

    """Return the list of neighbors, ordered by phermones.

    get_phermones_per_neighbor(self.get_neighbors())[0][0] will be the location of the highest phermone neighbor

    returns: a list of 2-length tuples of 2-length location tuples and corresponding phermone levels, sorted with highest level first
    """
    def get_phermones_per_neighbor(self, possible_locs):
        # print(self.get_neighbors())
        phermone_levels = []
        for l in possible_locs:
            if(l[0] > 0 and l[1] > 0 and l[0] <= self.sim.array.shape[0]-1 and l[1] <= self.sim.array.shape[1]-1):
                loc_level = min(self.sim.array[*l],self.phermone_max)
                phermone_levels.append((l,loc_level))

        # _ = [print(self.sim.array[l]) for l in self.get_neighbors()]
        phermone_levels.sort(key=lambda level:level[1],reverse=True)
        # print(phermone_levels[0][0])
        # print(phermone_levels)
        return phermone_levels

    """Move forward (toward current direction)
    """
    def move_forward(self):
        self.location = np.add(self.location, self.directions[self.direction])
        # print(self.location)
        return self.location

    """Move while following
    """
    def move_follow(self):
        new_location = np.add(self.location, self.directions[self.direction])
        if(self.sim.array[*new_location] < self.trail_level):
            # print(self.direction)
            # possible_directions = (self.directions[self.direction], self.directions[(self.direction-1) % 8],self.directions[(self.direction + 1) % 8])
            possible_directions = [self.directions[(self.direction + i) % 8] for i in range(-2,3)]
            # print(possible_directions)
            possible_neighbors = [np.add(self.location, d) for d in possible_directions]
            neighbor_phermones = self.get_phermones_per_neighbor(possible_neighbors)
            # print(neighbor_phermones)
            if(len(neighbor_phermones) == 0):
                return self.sim.remove_ant(self)
            new_location = neighbor_phermones[0][0]
            self.direction = np.where(self.directions == np.subtract(new_location,self.location))[0][0]
            if(len(neighbor_phermones) > 1):
                if(neighbor_phermones[0][1] == neighbor_phermones[1][1]):
                    self.move_explore()
            # self.direction = self.directions

            return self.move_forward()


        else:
            if(self.fidelity_test()):
                return self.move_forward()
            else:
                return self.move_explore()


    """Move while exploring (random turn)
    """
    def move_explore(self):
        probs = [1, 2, 4, 2, 1]
        probs = [p/sum(probs) for p in probs]
        turn_choice = np.random.choice(range(-2,3),p=probs)
        # print(turn_choice)
        new_direction = self.direction + turn_choice
        new_direction = new_direction % 8
        # print(new_direction)
        return self.move_forward()


    """Movement behavior for each step

    Not gonna lie, this is a hot mess that needs more documentation.
    """
    def step(self):
        # self.move_forward()
        if(self.following):
            # print("following")
            if(self.fidelity_test()):
                # continue following
                self.move_follow()
            else:
                # wander off
                self.following = False
                self.move_explore()
        else:
            # move
            # print("not following")
            if(self.fidelity_test()):
                # begin following
                self.following = True
                # self.move_forward()
                # print(self.get_phermones_per_neighbor(self.get_neighbors()))
                # print(self.location)
                nbr_phers = self.get_phermones_per_neighbor(self.get_neighbors())
                # print(best_neighbor)
                # print(np.subtract(self.location,best_neighbor))
                # self.direction = np.where(self.directions == np.subtract(self.location,best_neighbor))[0][0]
                # dirs = [np.where(self.directions == np.subtract(self.location,i[0])) for i in nbr_phers]
                nbrs = [i[0] for i in nbr_phers]
                d_coords = list([np.subtract(self.location, n) for n in nbrs])
                # print(d_coords)

                dirs = []
                for d in d_coords:
                    for i in range(len(self.directions)):
                        j = self.directions[i]
                        if(d[0]==j[0] and d[1] == j[1]):
                            dirs.append(i)
                phers = [i[1] for i in nbr_phers]
                phers = phers/np.sum(phers)
                self.direction = np.random.choice(dirs, p=phers)
                # self.move_forward()
                # print(self.direction)
            else:
                # continue exploring
                self.move_explore()

        # print(self.sim.array.shape)

        # If ant location is outside space bounds, remove this ant from the simulation
        if(self.location[0] < 0 or self.location[1] < 0 or self.location[0] >= self.sim.array.shape[0]-1 or self.location[1] >= self.sim.array.shape[1]-1):
            self.sim.remove_ant(self)

        self.sim.deposit_phermone(self.location)
        # print(self.direction)

        return self.location