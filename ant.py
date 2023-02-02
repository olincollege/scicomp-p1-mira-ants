import numpy as np
from scipy.signal import convolve2d
import random
class Ant:
    def __init__(self, space, location = (0,0)):
        self.location = location
        self.following = False
        self.space = space
        self.neighbor_kernel = np.ones((3,3))
        self.neighbor_kernel[1,1] = 0

    def choose_phermone(self):
        pher_level = self.space[self.location]
        return random.random() < pher_level

    def get_neighbors(self):
        location_array = np.zeros_like(self.space.space)
        location_array[self.location] = 1
        neighbors = convolve2d(location_array, self.neighbor_kernel).nonzero()
        return list(zip(neighbors[0],neighbors[1]))

    def choose_most_phermones_neighbor(self):
        phermone_levels = [(l,self.space.space[l]) for l in self.get_neighbors()]
        phermone_levels.sort(key=lambda level:level[1],reverse=True)
        print(phermone_levels)
        return phermone_levels[0][0]


    def step(self):
        if(self.following):
            if(self.choose_phermone()):
                # continue following
                pass
            else:
                # wander off
                self.following = False
        else:
            # move
            if(self.choose_phermone()):
                # begin following
                self.following = True
            else:
                # continue exploring
                pass

        return self.location