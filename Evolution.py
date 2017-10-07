from World import World
from Agent import Agent
import math


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
