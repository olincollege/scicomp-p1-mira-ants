import numpy as np
from scipy.signal import convolve2d
import random
class Ant:
    def __init__(self, sim, fidelity_min, fidelity_max, phermone_max, trail_level, turning_kernel):
        """Initialize the ant.

        Note: Type and range restrictions are included in docstrings, but are not enforced. If these bounds are not followed, unexpected behavior may occur.

        Args:
            self
            sim: the Simulation object the ant is a part of (for calling simulation modifying functions)
            fidelity_min: float decimal between 0 and 1, the minimum chance of self.fidelity_test() returning true
            fidelity_max: float decimal between 0 and 1, the maximum chance of self.fidelity_test() returning true
            phermone_max: integer, the maximum quantity of phermones that the ant can sense
            trail_level: integer, the minimum phermone level that the ant will consider to be following a trail
            turning_kernel:
        Returns:
            none
        """
        self.location = np.int_(np.round(np.divide(sim.array.shape,2)))
        self.following = False
        self.fidelity_min = fidelity_min
        self.fidelity_max = fidelity_max
        self.phermone_max = phermone_max
        self.sim = sim
        self.trail_level = trail_level
        self.turning_kernel = [1,2,3,4,3,2,1]

        # Directions that the ant can be pointing, in vector form
        self.directions = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        # Directions Indices
        # 012
        # 7 3
        # 654

        # Start in a random direction
        self.direction = np.random.randint(0,8)

    def fidelity_test(self):
        """Make a decision based on the local phermone count and the fidelity.

        Note: The probability of returning True is bound by self.fidelity_min and self.fidelity_max.
        The probability is the local phermone level divided by self.phermone_max.

        Args:
            self
        Returns:
            a boolean representing the result of the ant's fidelity check.
        """

        # Get local pher_level
        pher_level = self.sim.array[*self.location]

        # Probability of True is phermone level divided by self.phermone_max
        pher_frac = pher_level/self.phermone_max

        # That probability is bound by self.fidelity_min and self.fidelity_max
        pher_frac = min(self.fidelity_max,pher_frac)
        pher_frac = max(self.fidelity_min,pher_frac)

        # Return True with probability pher_frac
        return (np.random.choice([True, False], p=[pher_frac,1-pher_frac]))

    def get_neighbors(self):
        """Get location of all neighbors.

        Args:
            self
        Returns:
            a list of 2-length arrays specifying neighbor locations
        """

        # Element-wise add self.location and direction, make a list iterating over directions
        return [np.add(self.location, self.directions[i]) for i in range(0,8)]

    def get_phermones_per_neighbor(self, possible_locs):
        """Return the list of neighbors, ordered by the phermone level at those locations.

        get_phermones_per_neighbor(self.get_neighbors())[0][0] will be the location of the highest phermone neighbor (although may be tied with others)

        Args:
            possible_locs: an iterable of 2-length iterables representing each possible location
        Returns:
            a list of 2-length tuples of 2-length location tuples and corresponding phermone levels, sorted with highest level first
        """

        # array to append to
        phermone_levels = []

        # for each possible location
        for l in possible_locs:
            # If the possible location is within the bounds, then...
            # This should always be true because the ant should never be allowed on the edge of the space, but it's here for safety
            if(l[0] > 0 and l[1] > 0 and l[0] <= self.sim.array.shape[0]-1 and l[1] <= self.sim.array.shape[1]-1):
                # level at location is the phermone array, limited by self.phermone_max
                loc_level = min(self.sim.array[*l],self.phermone_max)
                # and append
                phermone_levels.append((l,loc_level))


        phermone_levels.sort(key=lambda level:level[1],reverse=True)
        return phermone_levels

    def move_forward(self):
        """Move forward (toward current direction)

        Args:
            self
        Returns:
            2-length array self.location
        """
        # element-wise add current location and direction vector of current direction
        self.location = np.add(self.location, self.directions[self.direction])
        return self.location

    def calc_direction(self, test_location):
        """Calculate what direction a test location is from ant's current location

        Args:
            self
            test_location: a 2-length array
        Returns
            2-length array, the direction of the test location
        """

        # Get a list of 2-length boolean vectors of whether each direction matches the difference between the two locations
        # Not gonna lie, this is a bit of code magic I don't fully understand
        direction_bool_vecs = self.directions == np.subtract(test_location,self.location)
        # Create a new list of whether both booleans are true
        direction_bools = [i[0] and i[1] for i in direction_bool_vecs]
        # Direction is where value is true
        direction = np.where(direction_bools)[0][0]
        return direction



    def move_follow_braden(self):
        """This was created to test my following code, and is me directly coding from the notes in Braden's presentation.

        I did this because I was troubleshooting my following algorithm and I was peer reviewing his presentation. I don't claim this as orignal.
        In the end, this ended up having the same behavior as my fixed following algorithm.
        I have not properly commented this as it is not "production" code. I just didn't want to delete it.
        """
        possible_directions = [self.directions[(self.direction + i) % 8] for i in [-1,0,1]]
        # print(possible_directions)
        possible_neighbors = [np.add(self.location, d) for d in possible_directions]
        neighbor_phermones = self.get_phermones_per_neighbor(possible_neighbors)

        if(len(neighbor_phermones) == 0):
            self.sim.remove_ant(self)
            print("something went wrong")

        elif(len(neighbor_phermones) == 1):
            new_location = neighbor_phermones[0][0]
            self.direction = self.calc_direction(new_location)
            self.move_forward()
        else:

            forward_location = np.add(self.location, self.directions[self.direction])
            max_location = neighbor_phermones[0][0]
            # print(forward_location)
            # print(max_location)

            if(max_location[0] == forward_location[0] and max_location[1] == forward_location[1]):
                self.move_forward()
            elif(neighbor_phermones[0][1] == neighbor_phermones[1][1]):
                self.move_explore()
            else:
                new_location = max_location
                self.direction = self.calc_direction(new_location)
                self.move_forward()

        return None

    def move_follow(self):
        """Do the logic for the ant's movement while following

        Args:
            self
        Returns:
            2-length array of self.location, passed from self.move_forward
            OR None, the return value of list.return()
        """
        # Location to test is right in front of us
        new_location = np.add(self.location, self.directions[self.direction])

        # If right in front of us is not a trail
        if(self.sim.array[*new_location] < self.trail_level):

            # Possible directions are forward and left, forward, or forward and right. Make a list of the vector directions
            possible_directions = [self.directions[(self.direction + i) % 8] for i in [-1,0,1]]
            # Add each vector direction to the current location to get a vector of possible end locations
            possible_neighbors = [np.add(self.location, d) for d in possible_directions]
            # Get the phermone levels of the neighbors
            neighbor_phermones = self.get_phermones_per_neighbor(possible_neighbors)
            # If the length of the phermone levels is zero, we must have reached the edge and must be removed. This should never happen, but was here from troubleshooting
            if(len(neighbor_phermones) == 0):
                return self.sim.remove_ant(self)

            # New location is the first (and therefore highest, because get_phermones_per_neighbor sorts) neighbor
            new_location = neighbor_phermones[0][0]

            # Update direction to be towards most phermone neighbor
            self.direction = self.calc_direction(new_location)

            # If multipe neighbors (this should always be true but this is a safety from testing)
            if(len(neighbor_phermones) > 1):
                # If the 2 highest phermone levels are equal
                if(neighbor_phermones[0][1] == neighbor_phermones[1][1]):
                    # Then behave as if exploring
                    return self.move_explore()

            # If we didn't explore, then move forward and end step
            return self.move_forward()
        # If in front of us is a valid trail, then...
        else:
            # Do a fidelity test. If that returns True, then follow the trail. If it returns False, behave as if exploring
            if(self.fidelity_test()):
                return self.move_forward()
            else:
                return self.move_explore()


    """Move while exploring (random turn)
    """
    def move_explore(self):
        """Move according to exploring logic.

        While exploring, ants choose a random direction according to the turning kernel

        Args:
            self
        Returns:
            a 2-length array, self.location passed from self.move_forward
        """
        # Calculate the fractional probability for the turning kernel. This allows turning kernel to be anything, even though we need probabilities that sum to one
        prob_fracs = [p/sum(self.turning_kernel) for p in self.turning_kernel]
        # l is length of turning kernel
        l = len(self.turning_kernel)
        # Low side of the range is negative one half of one less than the length. For the default turning kernel of [1,2,3,4,3,2,1], that is -3
        lo = -(l-1)/2
        # High side of the range is one half of one more than the length. For the default, that is 4.
        hi = (l+1)/2

        # Randomly choose a turn direction
        turn_choice = np.random.choice(range(lo,hi),p=prob_fracs)
        # New direction index
        new_direction = self.direction + turn_choice
        new_direction = new_direction % 8

        # Set self.direction
        self.direction = new_direction

        # Move forward
        return self.move_forward()

    """Movement behavior for each step

    Not gonna lie, this is a hot mess that needs more documentation.
    """
    def step(self):
        # If we are currently following, do a fidelity test for whether we continue following or decide to explore
        if(self.following):
            if(self.fidelity_test()):
                # continue following
                self.move_follow()
            else:
                # wander off
                self.following = False
                self.move_explore()
        else:
            if(self.fidelity_test()):
                # begin following
                self.following = True

                # Get all neighbors and phermones
                nbr_phers = self.get_phermones_per_neighbor(self.get_neighbors())
                # Get location for each phermone
                nbrs = [i[0] for i in nbr_phers]
                # Get direction vectors
                d_coords = list([np.subtract(self.location, n) for n in nbrs])

                dirs = []
                # Get the direction choices. I don't understand what I did here and I don't want to decode it.
                for d in d_coords:
                    for i in range(len(self.directions)):
                        j = self.directions[i]
                        if(d[0]==j[0] and d[1] == j[1]):
                            dirs.append(i)
                phers = [i[1] for i in nbr_phers]
                phers = phers/np.sum(phers)
                # Choose a direction to begin following next turn.
                self.direction = np.random.choice(dirs, p=phers)
            else:
                # continue exploring
                self.move_explore()

        # If we are outside the allowed coordinates, remove this ant. Ants may not be on the border locations or outside the simulation array
        if(self.location[0] < 1 or self.location[1] < 1 or self.location[0] >= self.sim.array.shape[0]-2 or self.location[1] >= self.sim.array.shape[1]-2):
            return self.sim.remove_ant(self)

        # Tell the simulation to deposit phermone
        self.sim.deposit_phermone(self.location)

        return self.location