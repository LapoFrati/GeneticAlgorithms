from Bedau.World import World
from Bedau.Agent import Agent
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import animation
from datetime import datetime as dt
import numpy as np
import math
import random


class Population():
    def __init__(self, world_size, pop_size, mutation_rate, meta_mutation, meta_mutation_range, resource_freq, iterations, seed=None):
        self.world_size = world_size
        # mutation rate: μ
        self.mutation_rate = mutation_rate
        # mutation rate of mutation: μ_μ
        self.meta_mutation = meta_mutation
        # mutation rate varies in [μ-ε,μ+ε]: ε
        self.meta_mutation_range = meta_mutation_range
        # possible behaviours are 1-15 steps in 8 compass direction + (0,0)
        self.behaviours = [(0, 0, 0, 0)]
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
        self.iterations = iterations
        self.log = np.zeros((1024, 121, self.iterations))
        for i in range(0, pop_size):
            self.population.append(
                Agent(world_size=self.world_size,
                      behaviours=self.behaviours,
                      mutation_parameters=(
                          self.mutation_rate, self.meta_mutation, self.meta_mutation_range),
                      world=self.world,
                      random_source=self.random_source,
                      log=self.log))
        self.history = []

    def evolve(self, plotting=False):
        for idx in range(self.iterations):
            # check if resources must be updated at current iteration
            if idx % self.resource_freq == 0:
                self.world.generate_resources(self.world.random_location())
            if idx > 0:
                # copy the previous population values to be updated
                self.log[:, :, idx] = self.log[:, :, idx - 1]
            self.update_pop(idx)
            if plotting:
                self.log_history()
            self.print_pop(idx)
            if len(self.population) == 0:
                break
        if plotting:
            self.plot_history()
        print("\nSeed: {}\n".format(self.seed))

    def update_pop(self, iteration):
        new_pop = []
        # shuffle to avoid giving proiority to any specific agent during update
        self.random_source.shuffle(self.population)
        for agent in self.population:
            state, child = agent.update(iteration)
            if(state == True):
                new_pop.append(agent)
                if(child is not None):
                    new_pop.append(child)
        self.population = new_pop

    def print_pop(self, iteration):
        print("---------------------")
        print("Iteration: {}".format(iteration))
        print("Pop size: {}".format(len(self.population)))
        print("Residual resource: {}".format(self.world.residual_resource()))
        # history_slice = np.zeros((121, 1024))
        # for agent in self.population:
        #     for idx, behaviour in enumerate(agent.sensory_motor_map):
        #         history_slice[behaviour[3]][idx] += 1
        # print(history_slice)
        # self.world.print_world()

    def log_history(self):
        temp = []
        for agent in self.population:
            temp.append((agent.position[1], agent.position[0]))
        locations = np.array(temp)
        self.history.append((np.array(self.world.world), locations))

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
