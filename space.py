import numpy as np
import ant

class Space:
    def __init__(self, shape):
        # self.space = np.zeros(shape=shape)
        self.array = np.random.randint(0,10,size=shape)


    def step(self):
        # self.array = np.max(self.array-1,0)
        # self.array = np.array(list(map(lambda x:max(x,0), self.array)))
        stepdown = np.vectorize(lambda x:max(x-1,0))
        self.array = stepdown(self.array)
        return self.array

    def loop(self, n):
        return [self.step() for _ in range(n)]