import numpy as np
from ant import Ant
import time

class Simulation:
    def __init__(self, shape):
        self.array = np.int_(np.zeros(shape=shape))
        # print(self.array)
        # self.array = np.random.randint(0,10,size=shape)
        # self.ants = [Ant(self) for _ in range(n)]
        self.ants = []
        # print(self.array)

    def step(self):
        self.ants.append(Ant(self))
        [a.step() for a in self.ants]

        stepdown = np.vectorize(lambda x:max(x-1,0))
        self.array = stepdown(self.array)
        return self.array

    def deposit_phermone(self, loc, n = 3):
        # print(loc)
        # print(self.array[*loc])
        self.array[*loc] += n
        # print(self.array)
        return self.array[*loc]

    def remove_ant(self, ant):
        self.ants.remove(ant)

    def loop(self, n):
        # return [self.step() for _ in range(n)]
        for _ in range(n):
            print(self.step())
            time.sleep(1)
