from Evolution import Evolution

behaviours = []


def main():
    print("Start")
    world_size = 128
    pop_size = 100
    mutation_rate = 0.01
    meta_mutation = 0.01
    meta_mutation_range = 0.0025  # from paper
    evol = Evolution(world_size=world_size, pop_size=pop_size, mutation_rate=mutation_rate,
                     meta_mutation=meta_mutation, meta_mutation_range=meta_mutation_range)
    evol.iterate(100)
    print("End")


if __name__ == '__main__':
    main()
