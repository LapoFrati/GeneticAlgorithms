from Bedau.Population import Population
from Bedau.Log import Log


def main():
    print("Start")
    world_size = 128
    pop_size = 1000
    mutation_rate = 0.1
    meta_mutation = 0.66
    meta_mutation_range = 0.0025  # from paper
    resource_freq = 1
    plotting = False
    iterations = 1000
    pop_log = Population(world_size=world_size,
                         pop_size=pop_size,
                         mutation_rate=mutation_rate,
                         meta_mutation=meta_mutation,
                         meta_mutation_range=meta_mutation_range,
                         resource_freq=resource_freq,
                         iterations=iterations,
                         plotting=plotting).evolve()

    if plotting:
        pop_log.plot()

    print("End")


if __name__ == '__main__':
    main()
