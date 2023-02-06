import numpy as np
from ant import Ant
import time

class Simulation:
    def __init__(self, shape=(15,15), phermone_deposit_rate = 4, fidelity = 5, phermone_limit = 10):
        self.array = np.int_(np.zeros(shape=shape))

        self.phermone_deposit_rate = phermone_deposit_rate
        self.fidelity = fidelity
        self.phermone_limit = phermone_limit
        # print(self.array)
        # self.array = np.random.randint(0,10,size=shape)
        # self.ants = [Ant(self) for _ in range(n)]
        self.ants = []
        # print(self.array)

    def step(self):
        self.ants.append(Ant(self, fidelity=self.fidelity, phermone_limit=self.phermone_limit))
        [a.step() for a in self.ants]

        stepdown = np.vectorize(lambda x:max(x-1,0))
        self.array = stepdown(self.array)
        return self.array

    def deposit_phermone(self, loc, n=None):
        # print(loc)
        # print(self.array[*loc])
        if(n):
            self.array[*loc] += n
        else:
            self.array[*loc] += self.phermone_deposit_rate
        # print(self.array)
        return self.array[*loc]

    def remove_ant(self, ant):
        self.ants.remove(ant)

    def loop(self, n = 10, print_iter = False, sleep = None):
        # return [self.step() for _ in range(n)]
        for _ in range(n):
            if(print):
                print(self.step())
            if(sleep):
                time.sleep(sleep)
