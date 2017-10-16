from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import animation
from datetime import datetime as dt
import numpy as np


class Log():
    def __init__(self, iterations, plot_world=False):
        self.iterations = iterations
        self.plot_world = plot_world
        self.track_world = []
        self.track_population = []
        self.track_residual = []
        self.track_mutations = []
        self.track_sensory = np.zeros((1024, 121, self.iterations))
        self.time = dt.now()

    def log_sensory(self, sensory_state, behaviour, iteration, val):
        self.track_sensory[sensory_state, behaviour, iteration] += val

    def copy_state(self, iteration):
        if iteration > 0:
            self.track_sensory[:, :,
                               iteration] = self.track_sensory[:, :, iteration - 1]

    def log_stats(self, world, population):
        residual = world.residual_resource()
        self.track_residual.append(residual)
        pop_size = len(population)
        self.track_population.append(pop_size)
        mean_mut = 0.
        temp = []
        for agent in population:
            mean_mut += agent.mutation_rate
            if self.plot_world:
                temp.append((agent.position[1], agent.position[0]))
        mean_mut /= pop_size
        self.track_mutations.append(mean_mut)
        if self.plot_world:
            locations = np.array(temp)
            self.track_world.append((np.array(world.world), locations))
        return residual, pop_size, mean_mut

    def plot(self):
        fig, ax = plt.subplots()
        ax = plt.axes(xlim=(0, 128), ylim=(0, 128))
        line1 = ax.imshow(self.track_world[0][0], shape=(128, 128),
                          interpolation='nearest', cmap=cm.coolwarm)
        line2 = ax.scatter([], [], s=10, c='red')

        def init():
            line1.set_array([[], []])
            line2.set_offsets([])
            return line1, line2

        def animate(i):
            line1.set_array(self.track_world[i][0])
            line2.set_offsets(self.track_world[i][1])
            return line1, line2

        anim = animation.FuncAnimation(fig, animate, frames=len(
            self.track_world), interval=300, blit=True, init_func=init, repeat=False)
        path_to_save = self.time.strftime('%Y-%m-%d_%H-%M') + '.mp4'
        print('Plotting track_world to ' + path_to_save)
        anim.save(path_to_save, fps=5, dpi=300,
                  extra_args=['-vcodec', 'libx264'])
        print('Plotting Finished')
