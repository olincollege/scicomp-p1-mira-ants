import numpy as np
from ant import Ant

class Space:
    def __init__(self, shape, n=1):
        self.array = np.int_(np.zeros(shape=shape))
        # print(self.array)
        # self.array = np.random.randint(0,10,size=shape)
        self.ants = [Ant(self) for _ in range(n)]
        # print(self.array)


    def step(self):
        [a.step() for a in self.ants]

        stepdown = np.vectorize(lambda x:max(x-1,0))
        self.array = stepdown(self.array)
        return self.array

    def deposit_phermone(self, loc, n = 1):
        # print(loc)
        # print(self.array[*loc])
        self.array[*loc] += n
        # print(self.array)
        return self.array[*loc]

    def loop(self, n):
        return [self.step() for _ in range(n)]