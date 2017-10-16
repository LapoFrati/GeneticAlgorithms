import copy


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
            self.sensory_motor_map = []  # sensory motor map: φ
            self.behaviours = behaviours
            self.world = world
            self.random_source = random_source
            self.log = log
            for i in range(0, 1024):
                pick = self.random_source.randint(len(behaviours))
                # initialize the log with stats of the initial population
                self.log.log_sensory(i, pick, 0, 1)
                self.sensory_motor_map.append(pick)
        else:
            # copy constructor
            self.position = orig.position
            self.resources = orig.resources
            self.mutation_rate = orig.mutation_rate
            self.meta_mutation = orig.meta_mutation
            self.meta_mutation_range = orig.meta_mutation_range
            self.sensory_motor_map = list(orig.sensory_motor_map)
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
        new_sensory_motor_map = []
        for idx, behaviour in enumerate(self.sensory_motor_map):
            if self.random_source.rand(1) < self.mutation_rate:
                new_behaviour = behaviour
                while(new_behaviour is behaviour):
                    new_behaviour = self.random_source.randint(
                        len(self.behaviours))
                    self.log.log_sensory(idx, new_behaviour, iteration, 1)
                new_sensory_motor_map.append(new_behaviour)
            else:
                self.log.log_sensory(idx, behaviour, iteration, 1)
                new_sensory_motor_map.append(behaviour)
        child.sensory_motor_map = new_sensory_motor_map

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
            for idx, behaviour in enumerate(self.sensory_motor_map):
                self.log.log_sensory(idx, behaviour, iteration, -1)
            return False, None
        if self.resources >= 500:
            return True, self.reproduce(iteration)
        else:
            return True, None
