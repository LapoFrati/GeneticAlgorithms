from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import animation
from datetime import datetime as dt
import numpy as np


class Log():
    def __init__(self, iterations, plot_world_flag=False):
        self.iterations = iterations
        self.plot_world_flag = plot_world_flag
        self.track_world = []
        self.track_population = []
        self.track_residual = []
        self.track_color = []
        self.track_mutations = []
        self.track_mutation_rates_high= []
        self.track_mutation_rates_highest= []
        self.track_mutation_rates_lowest= []
        self.track_mutation_rates_low= []
        self.track_mutation_rates_middle= []
        self.track_sensory = np.zeros((1024, 121, self.iterations))
        self.slice_support = np.arange(1024)

    def log_sensory(self, sensory_motor_map, iteration, val):
        self.track_sensory[self.slice_support,
                           sensory_motor_map, iteration] += val

    def copy_state(self, iteration):
        if iteration > 0:
            self.track_sensory[:, :,
                               iteration] = self.track_sensory[:, :, iteration - 1]

    def log_stats(self, world, population, color, mutations_high, mutations_low, mutations_middle, mutations_highest, mutations_lowest):
        residual = world.residual_resource()
        self.track_residual.append(residual)
        pop_size = len(population)
        self.track_population.append(pop_size)
        color = 0
        mutations_high = 0
        mutations_highest = 0
        mutations_low = 0
        mutations_lowest = 0
        mutations_middle = 0
        mean_mut = 0.
        temp = []
        for agent in population:
            mean_mut += agent.mutation_rate
            if self.plot_world_flag:
                temp.append((agent.position[1], agent.position[0]))
        mean_mut /= pop_size
        for agent in population:
            if agent.mutation_rate == 1:
                mutations_highest += 1
            elif agent.mutation_rate == 0.1:
                mutations_high += 1
            elif agent.mutation_rate == 0.01:
                mutations_middle += 1
            elif agent.mutation_rate == 0.001:
                mutations_low += 1
            else:
                mutations_lowest += 1
        for agent in population:
            if agent.color == 1:
                color += 1
        self.track_color.append(color)
        self.track_mutations.append(mean_mut)
        self.track_mutation_rates_highest.append(mutations_highest)
        self.track_mutation_rates_high.append(mutations_high)
        self.track_mutation_rates_low.append(mutations_low)
        self.track_mutation_rates_lowest.append(mutations_lowest)
        self.track_mutation_rates_middle.append(mutations_middle)
        if self.plot_world_flag:
            locations = np.array(temp)
            self.track_world.append((np.array(world.world), locations))
        return residual, pop_size, color, mean_mut, mutations_low, mutations_high, mutations_middle, mutations_lowest, mutations_highest

    def plot_world(self):
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
        time = dt.now()
        path_to_save = time.strftime('%Y-%m-%d_%H-%M') + '.mp4'
        print('Plotting track_world to ' + path_to_save)
        anim.save(path_to_save, fps=5, dpi=300,
                  extra_args=['-vcodec', 'libx264'])
        print('Plotting Finished')

    def plot_stats(self, save_stats=False):
        x = np.arange(self.iterations)
        f, axarr = plt.subplots(3, sharex=True)
        axarr[0].plot(x, self.track_residual)
        axarr[0].set_ylabel('Residual resources')
        axarr[1].plot(x, self.track_population)
        axarr[1].set_ylabel('Pop. size')
        axarr[2].plot(x, self.track_mutation_rates_high, 'r')
        axarr[2].plot(x, self.track_mutation_rates_highest, 'k')
        axarr[2].plot(x, self.track_mutation_rates_lowest, 'y')
        axarr[2].plot(x, self.track_mutation_rates_middle, 'b')
        axarr[2].plot(x, self.track_mutation_rates_low, 'g')
        axarr[2].set_ylabel('Mutation rates')
        axarr[2].set_xlabel('Iterations')

        for ax in axarr:
            # ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            # set vertical dashed lines to better check values across plots
            ax.grid(True, axis='x', linestyle='dashed')
            ax.get_yaxis().set_label_coords(-0.17, 0.5)

        # show x axis values only on last plot
        plt.setp([a.get_xticklabels() for a in axarr[:-1]], visible=False)
        if save_stats:
            time = dt.now()
            path_to_save = time.strftime('%Y-%m-%d_%H-%M') + '.pdf'
            print('Plotting stats to ' + path_to_save)
            plt.savefig(path_to_save, bbox_inches='tight')
            print('Plotting Finished')
        else:
            plt.tight_layout()
            plt.show()
