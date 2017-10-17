import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from numpy.random import randn
from matplotlib import cm
from datetime import datetime as dt
from Bedau.Evolution import Evolution
# First set up the figure, the axis, and the plot element we want to animate


#
world_size = 128
pop_size = 100
mutation_rate = 0.01
meta_mutation = 0.66
meta_mutation_range = 0.0025  # from paper
evol = Evolution(world_size=world_size, pop_size=pop_size, mutation_rate=mutation_rate,
                 meta_mutation=meta_mutation, meta_mutation_range=meta_mutation_range)
evol.iterate(50)

fig, ax = plt.subplots()
ax = plt.axes(xlim=(0, 128), ylim=(0, 128))
line1 = ax.imshow(evol.history[0][0], shape=(128, 128),
                  interpolation='nearest', cmap=cm.coolwarm)
line2 = ax.scatter([], [], s=10, c='red')


def init():
    line1.set_array([[], []])
    line2.set_offsets([])
    return line1, line2


def animate(i):
    line1.set_array(evol.history[i][0])
    line2.set_offsets(evol.history[i][1])
    return line1, line2


# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(
    fig, animate, frames=len(evol.history), interval=300, blit=True, init_func=init, repeat=False)

# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
#anim.save('basic_animation.mp4', fps=2, extra_args=['-vcodec', 'libx264'])

name = dt.now().strftime('%Y-%m-%d_%H-%M') + '.mp4'
anim.save(name, fps=5, dpi=300, extra_args=['-vcodec', 'libx264'])

# lt.show()
