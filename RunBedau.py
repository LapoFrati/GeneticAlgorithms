from Bedau.Population import Population
from Bedau.Log import Log


def main():
    print("Start")
    world_size = 128
    pop_size = 500
    mutation_rate = 0.01
    meta_mutation = 0.01
    resource_freq = 1
    plotting = False
    iterations = 50000
    pop_log = Population(world_size=world_size,
                         pop_size=pop_size,
                         mutation_rate=mutation_rate,
                         meta_mutation=meta_mutation,
                         resource_freq=resource_freq,
                         iterations=iterations,
                         plotting=plotting,
                         progress=True).evolve()

    if plotting:
        pop_log.plot_world()
    pop_log.plot_stats()

    print("End")


if __name__ == '__main__':
    main()
