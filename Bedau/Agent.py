import copy
import numpy as np


class Agent():

    def __init__(self, world_size=None, behaviours=None, mutation_parameters=None, world=None, random_source=None, log=None, orig=None):
        if orig is None:
            # current location: x
            self.position = world.random_location()
            self.resources = 250.  # current reservoir of resources: E
            # mutation rate of sensor_map's loci: μ
            self.mutation_rate = mutation_parameters[0]
            self.meta_mutation = mutation_parameters[1]
            self.meta_mutation_range = mutation_parameters[2]
            self.random_source = random_source
            self.behaviours = behaviours
            self.sensory_motor_map = self.random_source.randint(
                len(behaviours), size=1024, dtype=int)  # sensory motor map: φ
            self.log = log
            self.log.log_sensory(self.sensory_motor_map, 0, 1)
            self.world = world

        else:
            # copy constructor
            self.position = orig.position
            self.resources = orig.resources
            self.mutation_rate = orig.mutation_rate
            self.meta_mutation = orig.meta_mutation
            self.meta_mutation_range = orig.meta_mutation_range
            self.sensory_motor_map = np.array(
                orig.sensory_motor_map, dtype=int)
            self.behaviours = orig.behaviours
            self.world = orig.world
            self.random_source = orig.random_source
            self.log = orig.log

    def move(self, position, behaviour):
        # behaviour = (dx,dy, magnitude), discard the magnitude with [:2]
        self.position = tuple(map(lambda x, y: (x + y) %
                                  self.world.world_size, position, behaviour[:2]))

    def reproduce(self, iteration):
        self.resources /= 2
        # the child is going to have half of the resources of the parent
        child = Agent(orig=self)
        # mutate the sensory_motor_map
        num_mutations = self.random_source.binomial(1024, self.mutation_rate)
        loc_mutations = self.random_source.randint(1024, size=num_mutations)
        new_behaviors = self.random_source.randint(121, size=num_mutations)
        child.sensory_motor_map[loc_mutations] = new_behaviors
        self.log.log_sensory(child.sensory_motor_map, iteration, 1)

        # mutate the mutation rate
        if(self.random_source.rand(1) < self.meta_mutation):
            child.mutation_rate = self.random_source.uniform(
                max(0, self.mutation_rate - self.meta_mutation_range),
                min(1, self.mutation_rate + self.meta_mutation_range))

        return child

    def update(self, iteration):
        sensory_state = self.world.get_sensory_state(self.position)
        current_behaviour = self.sensory_motor_map[sensory_state]
        self.move(self.position, self.behaviours[current_behaviour])
        self.resources += self.world.probe(self.position) \
            - 20 - self.behaviours[current_behaviour][2]
        if self.resources <= 0:
            self.log.log_sensory(self.sensory_motor_map, iteration, -1)
            return False, None
        if self.resources >= 500:
            return True, self.reproduce(iteration)
        else:
            return True, None
