import numpy as np
from ant import Ant
import time
import matplotlib.pyplot as plt

class Simulation:

    """Create the simulation object

    `shape` (default (15,15)) is a 2-element tuple that specifies the size of the simulation space
    `phermone_deposit_rate` (default 4) is the amount of phermones deposited by an ant per time step
    `fidelity` (default 5) is the threshold for the fidelity check returning `True`
    `phermone_limit` (default 10) is the maximum phermone value that the ants can detect
    """
    def __init__(self, shape=(15,15), phermone_deposit_rate = 3, fidelity_min = 2, fidelity_max = 20, trail_level = 5):
        # self.array = np.int_(np.zeros(shape=shape))
        self.array = np.random.rand(*shape)

        self.phermone_deposit_rate = phermone_deposit_rate
        self.fidelity_min = fidelity_min
        self.fidelity_max = fidelity_max
        self.trail_level = trail_level
        # print(self.array)
        # self.array = np.random.randint(0,10,size=shape)
        # self.ants = [Ant(self) for _ in range(n)]
        self.ants = []
        # print(self.array)

    """Run a single step of the simulation, including phermone evaporation and ant steps
    """
    def step(self):
        self.ants.append(Ant(self, fidelity_min=self.fidelity_min, fidelity_max=self.fidelity_max, trail_level=self.trail_level))
        [a.step() for a in self.ants]
        # print(self.array)

        # This is a kinda cursed way to decrease the phermone level of the entire space by 1 bottoming out at 0
        stepdown = np.vectorize(lambda x:max(x-1.0,np.random.rand(1)[0]))
        self.array = stepdown(self.array)
        return self.array

    """Deposits an amount of phermone (n or self.phermone_deposit_rate) at the specified location
    """
    def deposit_phermone(self, loc, n=None):
        # print(loc)
        # print(self.array[*loc])
        if(n):
            self.array[*loc] += n
        else:
            self.array[*loc] += self.phermone_deposit_rate
        # print(self.array)
        return self.array[*loc]

    """Removes the specified ant from the simulation

    Ants are removed from the simulation when they wander outside the space
    """
    def remove_ant(self, ant):
        return self.ants.remove(ant)

    """Draw the simulation.
    """
    def draw(self):
        # Borrowed from Allen
        # https://raw.githubusercontent.com/AllenDowney/ThinkComplexity2/master/notebooks/Cell2D.py
        n, m = self.array.shape
        plt.axis([0, m, 0, n])
        ctr = np.int_(np.round(np.divide(self.array.shape,2)))
        arr = self.array.copy()
        # ctr[0] = ctr[0]-1
        # ctr[1] = ctr[1]+1
        arr[*ctr] = 0
        plt.imshow(arr, interpolation='none', origin='upper',extent=[0, m, 0, n])
        plt.show()


    """Loop the simulation.

    n (default 10) is the number of times to loop
    print_iter (default False) is whether to print the array at each loop
    sleep (default None) is the number of seconds to wait at each loop
    """
    def loop(self, n = 10, print_iter = False, sleep = None):
        # return [self.step() for _ in range(n)]
        for _ in range(n):
            if(print_iter):
                print(self.step())
            else:
                self.step()
            if(sleep):
                time.sleep(sleep)
