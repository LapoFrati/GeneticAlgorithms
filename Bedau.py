import random
import numpy as np
import math

behaviours = []


class World():
    def __init__(self, size):
        self.world_size = size
        self.lattice = np.zeros((size, size))
        self.meta_mutation = 0          # mutation rate of mutation: μ_μ
        self.meta_mutation_range = 0    # mutation rate varies in [μ-ε,μ+ε]: ε

    def generate_resources(self):
        x, y = random.choice(range(0, 128)), random.choice(range(0, 128))
        for dx in range(0, 8):
            for dy in range(0, 8):
                lattice[x + dx][y + dy] += 255 / min(abs(dx) + abs(dy), 8)

    def resource_quota(self, center, dx, dy):
        distance = abs(dx) + abs(dy)
        if distance < 8:
            return 255 * (1 - distance / 8)
        else:
            return 0.

    def sense(self, location):

    def access(self, pos):
        return lattice[pos[0] % self.world_size][pos[1] % self.world_size]


class Agent():

    def __init__():
        self.position = (random.choice(range(0, 128)),
                         random.choice(range(0, 128)))  # current location: x
        self.sensory_state = 0         # current sensory state: s
        self.resources = 0              # current reservoir of resources: E
        self.sensory_motor_map = []     # sensory motor map: φ
        self.current_beaviour = (0, 0)  # update pos: pos' = pos + behav
        self.mutation = 0               # mutation rate of sensor_map's loci: μ

    def sum(self, tuple_1, tuple_2):
        return tuple(map(operator.add, tuple_1, tuple_2))


def main():
    print("Start")
    print("End")


if __name__ == '__main__':
    main()
