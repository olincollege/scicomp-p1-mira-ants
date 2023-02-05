import numpy as np
from scipy.signal import convolve2d
import random
class Ant:
    def __init__(self, space, fidelity = 3, phermone_limit=None):
        self.location = np.int_(np.round(np.divide(space.array.shape,2)))
        self.following = False
        self.fidelity = fidelity
        self.space = space
        self.phermone_limit = phermone_limit
        # 012
        # 7 3
        # 654
        self.directions = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        self.direction = np.random.randint(0,7)
        self.neighbor_kernel = np.ones((3,3))
        self.neighbor_kernel[1,1] = 0

    def fidelity_test(self):
        pher_level = self.space.array[*self.location]
        # print(self.space.array)
        # print(pher_level)
        if(self.phermone_limit):
            if(self.phermone_limit < pher_level):
                pher_level = self.phermone_limit
        return pher_level < self.fidelity

    def get_neighbors(self):
        location_array = np.zeros_like(self.space.array)
        # print(self.location)
        location_array[self.location] = 1
        neighbors = convolve2d(location_array, self.neighbor_kernel).nonzero()
        return list(zip(neighbors[0],neighbors[1]))

    def choose_most_phermones_neighbor(self):
        phermone_levels = [(l,self.space.array[l]) for l in self.get_neighbors()]
        phermone_levels.sort(key=lambda level:level[1],reverse=True)
        # print(phermone_levels)
        return phermone_levels[0][0]


    def step(self):
        self.space.deposit_phermone(self.location)
        if(self.following):
            if(self.fidelity_test()):
                # continue following
                pass
            else:
                # wander off
                self.following = False
        else:
            # move
            if(self.fidelity_test()):
                # begin following
                self.following = True
            else:
                # continue exploring
                pass

        return self.location