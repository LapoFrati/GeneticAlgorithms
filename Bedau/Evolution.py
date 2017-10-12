from Bedau.World import World
from Bedau.Agent import Agent
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import animation
from datetime import datetime as dt
import numpy as np
import math
import random


class Evolution():
    def __init__(self, world_size, pop_size, mutation_rate, meta_mutation, meta_mutation_range, resource_freq, seed=None):
        self.world_size = world_size
        # mutation rate: μ
        self.mutation_rate = mutation_rate
        # mutation rate of mutation: μ_μ
        self.meta_mutation = meta_mutation
        # mutation rate varies in [μ-ε,μ+ε]: ε
        self.meta_mutation_range = meta_mutation_range
        # possible behaviours are 1-15 steps in 8 compass direction + (0,0)
        self.behaviours = [(0, 0, 0)]
        self.resource_freq = resource_freq
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

        self.time = dt.now()
        if seed is not None:
            self.seed = seed
        else:
            self.seed = random.SystemRandom().getrandbits(32)
        self.random_source = np.random.RandomState(self.seed)
        self.world = World(world_size, self.random_source)
        self.population = []
        for i in range(0, pop_size):
            self.population.append(
                Agent(self.world_size,
                      self.behaviours,
                      (self.mutation_rate, self.meta_mutation,
                       self.meta_mutation_range),
                      self.world, self.random_source))
        self.history = []

    def iterate(self, iterations, plotting=False):
        self.history = []
        self.mutations_counter = 0
        resources_timer = 0
        for idx in enumerate(range(iterations)):
            if resources_timer == 0:
                self.world.generate_resources(self.world.random_location())
            resources_timer = (resources_timer + 1) % self.resource_freq
            self.update_pop()
            self.log_history()
            self.print_pop()
            if len(self.population) == 0:
                break
        if plotting:
            self.plot_history()
        print("\nSeed: {}\n".format(self.seed))

    def log_history(self):
        temp = []
        for agent in self.population:
            temp.append((agent.position[1], agent.position[0]))
        locations = np.array(temp)
        self.history.append((np.array(self.world.world), locations))

    def update_pop(self):
        new_pop = []
        self.random_source.shuffle(self.population)
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
        print("---------------------")
        print("Iteration: {}".format(len(self.history)))
        print("Pop size: {}".format(len(self.population)))
        print("Residual resource: {}".format(self.world.residual_resource()))
        agents_resources = 0
        for agent in self.population:
            agents_resources += agent.resources
        print("Resources collected: {}".format(agents_resources))
        # self.world.print_world()

    def plot_history(self):
        fig, ax = plt.subplots()
        ax = plt.axes(xlim=(0, 128), ylim=(0, 128))
        line1 = ax.imshow(self.history[0][0], shape=(128, 128),
                          interpolation='nearest', cmap=cm.coolwarm)
        line2 = ax.scatter([], [], s=10, c='red')

        def init():
            line1.set_array([[], []])
            line2.set_offsets([])
            return line1, line2

        def animate(i):
            line1.set_array(self.history[i][0])
            line2.set_offsets(self.history[i][1])
            return line1, line2

        anim = animation.FuncAnimation(fig, animate, frames=len(
            self.history), interval=300, blit=True, init_func=init, repeat=False)
        path_to_save = self.time.strftime('%Y-%m-%d_%H-%M') + '.mp4'
        print('Plotting history to ' + path_to_save)
        anim.save(path_to_save, fps=5, dpi=300,
                  extra_args=['-vcodec', 'libx264'])
        print('Plotting Finished')
