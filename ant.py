import numpy as np
from scipy.signal import convolve2d
import random
class Ant:
    """Initialize the ant
    sim is the simulation the ant is a part of (for calling simulation modifying functions)
    See ant_simulation for parameter definitions
    """
    def __init__(self, sim, fidelity, phermone_limit, trail_level):
        self.location = np.int_(np.round(np.divide(sim.array.shape,2)))
        self.following = False
        self.fidelity = fidelity
        self.sim = sim
        self.phermone_limit = phermone_limit
        self.trail_level = trail_level

        # Directions that the ant can be pointing
        self.directions = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        # Directions Indices
        # 012
        # 7 3
        # 654

        # start in a random direction
        self.direction = np.random.randint(0,7)
        self.neighbor_kernel = np.int_(np.ones((3,3)))
        self.neighbor_kernel[1,1] = 0
        # print(self.neighbor_kernel)

    """Make a decision based on the local phermone count and the fidelity

    returns: boolean choice
    """
    def fidelity_test(self):
        pher_level = self.sim.array[*self.location]
        # print(self.sim.array)
        # print(pher_level)
        if(self.phermone_limit):
            if(self.phermone_limit < pher_level):
                pher_level = self.phermone_limit
        return pher_level < self.fidelity

    """Get location of each neighbor

    returns: a list of 2-length tuples specifying neighbor locations
    """
    def get_neighbors(self):
        location_array = np.zeros_like(self.sim.array)
        # print(self.location)
        location_array[*self.location] = 1
        neighbors = convolve2d(location_array, self.neighbor_kernel).nonzero()
        return list(zip(neighbors[0],neighbors[1]))

    """Return the neighbor with the highest number of phermones

    returns: a 2-length tuple
    """
    def choose_most_phermones_neighbor(self, possible_locs):
        # print(self.get_neighbors())
        phermone_levels = []
        for l in possible_locs:
            if(l[0] > 0 and l[1] > 0 and l[0] <= self.sim.array.shape[0]-1 and l[1] <= self.sim.array.shape[1]-1):
                loc_level = min(self.sim.array[*l],self.phermone_limit)
                phermone_levels.append((l,loc_level))

        # _ = [print(self.sim.array[l]) for l in self.get_neighbors()]
        phermone_levels.sort(key=lambda level:level[1],reverse=True)
        # print(phermone_levels[0][0])
        # print(phermone_levels)
        return phermone_levels[0][0]

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
            possible_directions = (self.directions[(self.direction-1) % 8],self.directions[(self.direction + 1) % 8])
            # print(possible_directions)
            possible_neighbors = [np.add(self.location, d) for d in possible_directions]
            self.location = self.choose_most_phermones_neighbor(possible_neighbors)
        else:
            return self.move_forward()


    """Move while exploring (random turn)
    """
    def move_explore(self):
        turn_choice = np.random.choice(range(-3,4),p=[0.04,0.06,0.2,0.4,0.2,0.06,0.04])

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
                # print(self.location)
                best_neighbor = self.choose_most_phermones_neighbor(self.get_neighbors())
                # print(best_neighbor)
                # print(np.add(np.subtract(self.location,best_neighbor),1))
                self.direction = np.where(self.directions == np.add(np.subtract(self.location,best_neighbor),1))[0][0]
                # print(self.direction)
            else:
                # continue exploring
                self.move_explore()

        # print(self.sim.array.shape)

        # If ant location is outside space bounds, remove this ant from the simulation
        if(self.location[0] < 0 or self.location[1] < 0 or self.location[0] >= self.sim.array.shape[0]-1 or self.location[1] >= self.sim.array.shape[1]-1):
            self.sim.remove_ant(self)

        self.sim.deposit_phermone(self.location)

        return self.location