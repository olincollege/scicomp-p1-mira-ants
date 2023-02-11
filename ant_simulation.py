"""This defile defines the Simulation object, which handles all simulation logic for the ant simulation.
"""

import numpy as np
from ant import Ant
import time
import matplotlib.pyplot as plt

class Simulation:
    def __init__(self,
                 shape=(256,256),
                 phermone_deposit_rate = 16,
                 phermone_evap_rate = 1,
                 fidelity_min = 0.01,
                 fidelity_max = 0.99,
                 phermone_max = 80,
                 trail_level = 8,
                 turning_kernel = [1,2,3,4,3,2,1]
                 ):
        """Create the simulation object.

        Note: Type and range restrictions are included in docstrings, but are not enforced. If these bounds are not followed, unexpected behavior may occur.

        Args:
            self
            shape (default (256,256)): 2-element tuple that specifies the size of the simulation space
            phermone_deposit_rate (default 16): integer amount of phermones deposited by an ant per time step
            phermone_evap_rate (default 1): integer amount of phermones that evaporate per cell over time
            fidelity_min (default 0.01): float decimal between 0 and 1, the minimum chance of self.fidelity_test() returning true
            fidelity_max (default 0.99): float decimal between 0 and 1, the maximum chance of self.fidelity_test() returning true
            phermone_max (default 80): integer, the maximum quantity of phermones that the ant can sense
            trail_level (default 8): integer, the minimum phermone level that the ant will consider to be following a trail
            turning_kernel (default [1,2,3,4,3,2,1]): the turning kernel to be used when exploring. Must be an odd length, and should be between 1 and 7 items long
        """

        # Array of phermones is specified by shape
        self.array = np.int_(np.zeros(shape=shape))

        self.phermone_deposit_rate = phermone_deposit_rate
        self.phermone_evap_rate = phermone_evap_rate
        self.fidelity_min = fidelity_min
        self.fidelity_max = fidelity_max
        self.phermone_max = phermone_max
        self.trail_level = trail_level
        self.turning_kernel = turning_kernel
        self.ants = []

    def step(self):
        """Run the main logic for the simulation step.

        Adds one ant. Step for each ant. Decreases phermone level by self.phermone_evap_rate.

        Args:
            self
        Returns:
            A np.ndarray, self.array
        """

        # Make a new ant
        self.ants.append(Ant(self,
                             fidelity_min=self.fidelity_min,
                             fidelity_max=self.fidelity_max,
                             phermone_max = self.phermone_max,
                             trail_level=self.trail_level,
                             turning_kernel=self.turning_kernel
                             ))
        # Step all ants
        [a.step() for a in self.ants]

        # This is a kinda cursed way to decrease the phermone level of the entire space by 1 bottoming out at 0
        stepdown = np.vectorize(lambda x:max(x-1.0,np.random.rand(1)[0]))
        self.array = stepdown(self.array)
        return self.array

    def deposit_phermone(self, loc):
        """Deposits self.phermone_deposit_rate of phermone at the specified location

        Args:
            self
            loc: a 2-length iterable, the location to deposit the phermone
        Returns:
            integer, the phermone level at the location being added to
        """
        self.array[*loc] += self.phermone_deposit_rate
        return self.array[*loc]

    def remove_ant(self, ant):
        """Removes the specified ant from the simulation

        Ants are removed from the simulation when they wander outside the space

        Args:
            self
            ant: the ant object to be removed
        Returns:
            none, returns value of list.remove()
        """
        return self.ants.remove(ant)

    def draw(self):
        """Draw the simulation. Borrowed from Allen Downey

        I added the behavior of drawing the center space as 0, because that space was getting the most phermones by far.

        Args:
            self
        Returns:
            none
        """
        # Borrowed from Allen
        # https://raw.githubusercontent.com/AllenDowney/ThinkComplexity2/master/notebooks/Cell2D.py
        n, m = self.array.shape
        plt.axis([0, m, 0, n])
        arr = self.array.copy()
        ctr = np.int_(np.round(np.divide(self.array.shape,2)))
        arr[*ctr] = 0
        plt.imshow(arr, interpolation='none', origin='upper',extent=[0, m, 0, n])


    def loop(self, n = 10, print_iter = False, sleep = None):
        """Loop the simulation.

        Args:
            n (default 10): integer, the number of times to loop
            print_iter (default False): boolean, whether to print the array at each loop
            sleep (default None): integer, the number of seconds to wait at each loop
        Returns:
            none
        """
        for _ in range(n):
            if(print_iter):
                print(self.step())
            else:
                self.step()
            if(sleep):
                time.sleep(sleep)
