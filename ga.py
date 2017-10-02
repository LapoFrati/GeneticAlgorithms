import random
import string
import functools
import sys


class Population():

    def generate_random_gene(self):
        return [random.choice(string.ascii_lowercase + ' ') for n in range(self.target_len)]

    def fitness(self, gene):
        score = 0
        for (candidate, expected) in zip(gene, self.target):
            if candidate == expected:
                score = score + 1
        return score

    def __init__(self, size, target):
        self.target = list(target)
        self.target_len = len(target)
        self.population = []
        self.population_size = size
        self.best_fitness = 0
        self.best_candidate = []

        for i in range(0, self.population_size):
            new_gene = self.generate_random_gene()
            new_fitness = self.fitness(new_gene)
            self.population.append((new_gene, new_fitness))
            if self.best_fitness < new_fitness:
                self.best_fitness = new_fitness
                self.best_candidate = new_gene

    def print_population(self):
        for gene, fitness in self.population:
            print(''.join(gene) + ' ' + str(fitness))

    def show_matches(self, candidate, target):
        matches = []
        for el1, el2 in zip(candidate, target):
            if el1 == el2:
                matches.append(el2)
            else:
                matches.append('.')
        return ''.join(matches)

    def track_progress(self, iteration='0'):
        local_best_fit = 0
        local_best_gene = []
        for (gene, fitness) in self.population:
            if local_best_fit < fitness:
                local_best_fit = fitness
                local_best_gene = gene
        self.best_candidate = local_best_gene
        self.best_fitness = local_best_fit
        print(iteration + "\tMatches: " + str(self.best_fitness) + ' \t' +
              self.show_matches(self.best_candidate, self.target))

    def mutate(self, gene):
        new_gene = []
        for el in gene:
            if random.random() < 2. / self.target_len:
                new_gene.append(random.choice(
                    (string.ascii_lowercase + ' ').replace(el, "")))
            else:
                new_gene.append(el)
        return new_gene

    def pure_chance(self):
        self.track_progress()
        for counter in range(0, 1000000):
            new_gene = self.generate_random_gene()
            new_fitness = self.fitness(new_gene)
            self.population.append((new_gene, new_fitness))
            if self.best_fitness < new_fitness:
                self.best_fitness = new_fitness
                self.best_candidate = new_gene
                self.track_progress(iteration=str(counter))

    def pure_mutation(self):
        self.track_progress()
        counter = 0
        while self.best_fitness < self.target_len:
            counter = counter + 1
            new_gene = self.mutate(self.best_candidate)
            new_fitness = self.fitness(new_gene)
            if self.best_fitness < new_fitness:
                self.best_fitness = new_fitness
                self.best_candidate = new_gene
                self.track_progress(iteration=str(counter))

    def next_iteration(self, elitism=False):
        wheel = Roulette(self.population)
        self.population = []
        if elitism:
            self.population.append((self.best_candidate, self.best_fitness))
        for i in range(len(self.population), self.population_size):
            candidate, candidate_fitnes = wheel.spin_roulette()
            offspring = self.mutate(candidate)
            offspring_fitness = self.fitness(offspring)
            if offspring_fitness > candidate_fitnes:
                self.population.append((offspring, offspring_fitness))
            else:
                self.population.append((candidate, candidate_fitnes))

    def iterate(self):
        i = 0
        while(self.best_fitness < self.target_len):
            self.next_iteration(elitism=True)
            self.track_progress(str(i))
            i = i + 1


class Roulette():
    def __init__(self, population):
        self.sum = 0
        self.wheel = []
        for gene, fitness in population:
            self.sum = self.sum + fitness
            self.wheel.append((gene, fitness, self.sum))

    def spin_roulette(self):
        pick = random.random() * self.sum
        for (gene, fitness, value) in self.wheel:
            if(value >= pick):
                return (gene, fitness)
        return random.choice(self.wheel)[:2]


        #pop = Population(100, "methinks it is like a weasel")
pop = Population(100, "fuck you darwin we have treedogs")
pop.print_population()
# pop.pure_chance()
# pop.pure_mutation()
pop.iterate()
