
import typing as tp
import numpy as np
Location = tp.Tuple[int, int]


class World():
    def __init__(self, world_size, random_source):
        self.world_size = world_size
        self.world = np.zeros((world_size, world_size), dtype=float)
        self.random_source = random_source
        self.peak_resource = 255
        self.bin_size = self.peak_resource / 4
        # add some resource pyramids to initialize the world
        for i in range(20):
            self.generate_resources(self.random_location())
        self.consumption_counter = 0.

    def generate_resources(self, loc: Location):
        """
        Generates a new pyramid of resources centered a the loc
        """
        for dx in range(-8, 8):
            for dy in range(-8, 8):
                distance = abs(dx) + abs(dy)
                if distance < 8:
                    resource = 255 * (1 - distance / 8)
                else:
                    resource = 0.
                self.set((loc[0] + dx, loc[1] + dy), resource)

    def sense(self, loc: Location):
        """
        Turns the amount of resources available in a location into 4 possible
        values (2 bits of indormation)

        Args:
            loc: location from which to extract the 2 bits of information
        Return:
            the two bits as an integer value
        """
        resources = self.get(loc)
        if(resources >= self.peak_resource):
            return 3
        else:
            return int(resources / self.bin_size)

    def get_sensory_state(self, loc: Location):
        """
        Builds the 10bit sensory state assembling the 2 bits of the current
        with the 8 bits coming from the 4 neighbours.
        Do so each value is shifted by 2 bits and then all the values are
        summed together to compute the final sensory state

        Args:
            loc: current location of the Agent
        Returns:
            sensory state
        """
        partial_state = []
        partial_state.append(self.sense(loc))
        partial_state.append(self.sense((loc[0] + 1, loc[1])) << 2)
        partial_state.append(self.sense((loc[0] - 1, loc[1])) << 4)
        partial_state.append(self.sense((loc[0], loc[1] - 1)) << 6)
        partial_state.append(self.sense((loc[0], loc[1] + 1)) << 8)
        return sum(partial_state)

    def get(self, loc: Location):
        """
        Gets the value at the specified position
        Args:
            loc: a tuple (x,y) that can be outside the limits of the world_size
        Returns:
            the resource at the corresponding location on the torus
        """
        return self.world[loc[0] % self.world_size][loc[1] % self.world_size]

    def set(self, loc: Location, increment: float):
        """
        Sets the resource at the specified position to value
        Args:
            loc: a tuple (x,y) that can be outside the limits of the world_size
            increment: amount to add in the specified position
        """
        self.world[loc[0] % self.world_size][loc[1] %
                                             self.world_size] += increment

    def probe(self, loc):
        resource_available = self.get(loc)
        resource_to_collect = min(resource_available, 100)
        self.set(loc, -resource_to_collect)
        return resource_to_collect

    def print_world(self):
        for row in self.world:
            print(''.join(map(lambda x: str(int(x)).ljust(4), row)))

    def random_location(self):
        return (self.random_source.choice(self.world_size),
                self.random_source.choice(self.world_size))

    def residual_resource(self):
        return self.world.sum()
