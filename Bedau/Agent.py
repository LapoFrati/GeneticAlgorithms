import copy


class Agent():

    def __init__(self, world_size, behaviours, mutation_parameters, world, random_source):
        # current location: x
        self.position = world.random_location()
        self.sensory_state = 0              # current sensory state: s
        self.resources = 250.               # current reservoir of resources: E
        self.current_behaviour = (0, 0, 0)  # update loc: loc' = loc + behav
        # mutation rate of sensor_map's loci: μ
        self.mutation_rate = mutation_parameters[0]
        self.meta_mutation = mutation_parameters[1]
        self.meta_mutation_range = mutation_parameters[2]

        self.sensory_motor_map = []     # sensory motor map: φ
        self.behaviours = behaviours
        self.world = world
        self.random_source = random_source

        for i in range(0, 1024):
            pick = self.random_source.randint(len(behaviours))
            self.sensory_motor_map.append(behaviours[pick])

    def move(self, tuple_1, tuple_2):
        self.position = tuple(map(lambda x, y: (x + y) %
                                  self.world.world_size, tuple_1, tuple_2[:2]))

    def mutate(self):
        self.resources /= 2
        # the child is going to have half of the resources of the parent
        child = copy.deepcopy(self)
        child.world = self.world
        # mutate the sensory_motor_map
        new_sensory_motor_map = []
        for behaviour in self.sensory_motor_map:
            if self.random_source.rand(1) < self.mutation_rate:
                new_behaviour = behaviour
                while(new_behaviour is behaviour):
                    pick = self.random_source.randint(len(self.behaviours))
                    new_behaviour = self.behaviours[pick]
                new_sensory_motor_map.append(new_behaviour)
            else:
                new_sensory_motor_map.append(behaviour)
        child.sensory_motor_map = new_sensory_motor_map

        # mutate the mutation rate
        if(self.random_source.rand(1) < self.meta_mutation):
            child.mutation_rate = self.random_source.uniform(
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
