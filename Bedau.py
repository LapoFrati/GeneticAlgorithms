import random
import numpy as np
import math
import typing as tp
import copy
import operator
Location = tp.Tuple[int, int]

behaviours = []


class Evolution():
    def __init__(self, world_size, pop_size, mutation_rate, meta_mutation, meta_mutation_range):
        self.world_size = world_size
        # mutation rate: μ
        self.mutation_rate = mutation_rate
        # mutation rate of mutation: μ_μ
        self.meta_mutation = meta_mutation
        # mutation rate varies in [μ-ε,μ+ε]: ε
        self.meta_mutation_range = meta_mutation_range
        # possible behaviours are 1-15 steps in 8 compass direction + (0,0)
        self.behaviours = [(0, 0, 0)]
        self.world = World(world_size)
        coeff = math.sqrt(2)
        for inc in range(1, 16):
            self.behaviours.append((inc, 0, inc))
            self.behaviours.append((-inc, 0, inc))
            self.behaviours.append((0, inc, inc))
            self.behaviours.append((0, -inc, inc))
            magnitude = coeff * inc
            self.behaviours.append((inc, inc, magnitude))
            self.behaviours.append((-inc, -inc, magnitude))
            self.behaviours.append((inc, -inc, magnitude))
            self.behaviours.append((-inc, inc, magnitude))

        self.population = []
        for i in range(0, pop_size):
            self.population.append(
                Agent(self.world_size, self.behaviours,
                      (self.mutation_rate, self.meta_mutation, self.meta_mutation_range), self.world))

    def iterate(self, iterations):
        for n in range(0, iterations):
            self.world.generate_resources(self.world.random_location())
            self.update_pop()
            self.print_pop()

    def update_pop(self):
        new_pop = []
        for agent in self.population:
            state, child = agent.update()
            if(state == True):
                new_pop.append(agent)
            if(child is not None):
                new_pop.append(child)
        self.population = new_pop

    def print_pop(self):
        # for idx, agent in enumerate(self.population):
        #    print("agent {}: {}".format(idx, agent.resources))
        print("Pop size: {}".format(len(self.population)))
        print("Residual resource: {}".format(self.world.residual_resource()))


class World():
    def __init__(self, world_size):
        self.world_size = world_size
        self.world = np.zeros((world_size, world_size), dtype=int)
        self.peak_resource = 255
        self.bin_size = self.peak_resource / 4

    def generate_resources(self, loc: Location):
        """
        Generates a new pyramid of resources centered a the loc
        """
        for dx in range(-8, 8):
            for dy in range(-8, 8):
                self.set((loc[0] + dx, loc[1] + dy),
                         self.resource_quota(dx, dy))

    def resource_quota(self, dx: int, dy: int):
        """
        Computes the amount of resources to add in the location based on the
        manhattan distance from the peak. The value peaks at 255 when dx=0 dy=0
        and falls linearly up to a distance of 8

        Args:
            dx: displacement on the x-axis
            dy: displacement on the y-axis

        Returns:
            the amount of resource to add in the location,
        """
        distance = abs(dx) + abs(dy)
        if distance < 8:
            return 255 * (1 - distance / 8)
        else:
            return 0.

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
            the corresponding location on the torus
        """
        return self.world[loc[0] % self.world_size][loc[1] % self.world_size]

    def set(self, loc: Location, value: float):
        """
        Sets the resource at the specified position to value
        Args:
            loc: a tuple (x,y) that can be outside the limits of the world_size
            value: amount to add in the specified position
        """
        self.world[loc[0] % self.world_size][loc[1] % self.world_size] += value

    def probe(self, loc):
        resource_available = self.get(loc)
        resource_to_collect = min(resource_available, 100)
        self.set(loc, - resource_to_collect)
        return resource_to_collect

    def print_world(self):
        for row in self.world:
            print(''.join(map(lambda x: str(int(x)).ljust(4), row)))

    def random_location(self):
        return (random.choice(range(0, self.world_size)), random.choice(range(0, self.world_size)))

    def residual_resource(self):
        return self.world.sum()


class Agent():

    def __init__(self, world_size, behaviours, mutation_parameters, world):
        # current location: x
        self.position = world.random_location()
        self.sensory_state = 0              # current sensory state: s
        self.resources = 0.                 # current reservoir of resources: E
        self.current_behaviour = (0, 0, 0)  # update loc: loc' = loc + behav
        # mutation rate of sensor_map's loci: μ
        self.mutation_rate = mutation_parameters[0]
        self.meta_mutation = mutation_parameters[1]
        self.meta_mutation_range = mutation_parameters[2]

        self.sensory_motor_map = []     # sensory motor map: φ
        self.behaviours = behaviours
        self.world = world

        for i in range(0, 1024):
            self.sensory_motor_map.append(random.choice(behaviours))

    def move(self, tuple_1, tuple_2):
        self.position = tuple(map(lambda x, y: (x + y) %
                                  self.world.world_size, tuple_1, tuple_2[:2]))

    def mutate(self):
        self.resources /= 2
        # the child is going to have half of the resources of the parent
        child = copy.deepcopy(self)

        # mutate the sensory_motor_map
        new_sensory_motor_map = []
        for behaviour in self.sensory_motor_map:
            if random.random() < self.mutation_rate:
                list_of_behaviours = list(self.behaviours)
                list_of_behaviours.remove(behaviour)
                new_sensory_motor_map.append(random.choice(list_of_behaviours))
            else:
                new_sensory_motor_map.append(behaviour)
        child.sensory_motor_map = new_sensory_motor_map

        # mutate the mutation rate
        if(random.random() < self.meta_mutation):
            child.mutation_rate = random.uniform(
                max(0, self.meta_mutation - self.meta_mutation_range),
                min(1, self.meta_mutation + self.meta_mutation_range))

        return child

    def update_resources(self):
        self.resources += self.world.probe(self.position) - \
            20 - self.current_behaviour[2]

    def update(self):
        self.sensory_state = self.world.get_sensory_state(self.position)
        self.current_behaviour = self.sensory_motor_map[self.sensory_state]
        self.move(self.position, self.current_behaviour)
        self.update_resources()
        if self.resources <= 0:
            return False, None
        if self.resources >= 500:
            return True, self.mutate()
        else:
            return True, None


def main():
    print("Start")
    world_size = 128
    pop_size = 100
    mutation_rate = 0.01
    meta_mutation = 0.01
    meta_mutation_range = 0.0025  # from paper
    evol = Evolution(world_size=world_size, pop_size=pop_size, mutation_rate=mutation_rate,
                     meta_mutation=meta_mutation, meta_mutation_range=meta_mutation_range)
    evol.iterate(100)
    print("End")


if __name__ == '__main__':
    main()
