from Bedau.Evolution import Evolution


def main():
    print("Start")
    world_size = 128
    pop_size = 100
    mutation_rate = 0.01
    meta_mutation = 0.66
    meta_mutation_range = 0.0025  # from paper
    evol = Evolution(world_size=world_size, pop_size=pop_size, mutation_rate=mutation_rate,
                     meta_mutation=meta_mutation, meta_mutation_range=meta_mutation_range)
    evol.iterate(1000, plotting=False)
    # TEST RESOURCE CONSUMPTION
    # evol.world.print_world()
    # evol.world.generate_resources((20, 20))
    # evol.print_pop()
    # evol.population[0].position = (21, 21)
    # evol.population[1].position = (20, 20)
    # evol.population[2].position = (19, 19)
    # evol.update_pop()
    # evol.update_pop()
    # evol.world.print_world()
    # evol.print_pop()
    print("End")


if __name__ == '__main__':
    main()
