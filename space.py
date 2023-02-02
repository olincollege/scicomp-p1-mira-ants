import numpy as np
import ant

class Space:
    def __init__(self, shape):
        # self.space = np.zeros(shape=shape)
        self.space = np.random.rand(*shape)


    def step(self):
        return self.space

    def loop(self, n):
        return [self.step() for _ in range(n)]