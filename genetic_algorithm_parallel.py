from mpi4py import MPI
import numpy as np
import pandas as pd
from genetic_algorithms_functions import calculate_fitness,     select_in_tournament, order_crossover, mutate,     generate_unique_population

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Load data only on root and broadcast
if rank == 0:
    distance_matrix = pd.read_csv('city_distances.csv').to_numpy()
    num_nodes = distance_matrix.shape[0]
else:
    distance_matrix = None
    num_nodes = None

distance_matrix = comm.bcast(distance_matrix, root=0)
num_nodes = comm.bcast(num_nodes, root=0)

# GA parameters
population_size = 10000
mutation_rate = 0.1
num_generations = 200
stagnation_limit = 5

# Generate initial population on root
if rank == 0:
    population = generate_unique_population(population_size, num_nodes)
else:
    population = None

for generation in range(num_generations):
    # Scatter population chunks to processes
    local_population = comm.scatter(np.array_split(population, size), root=0)

    # Local fitness evaluation
    local_fitness = np.array([calculate_fitness(ind, distance_matrix) for ind in local_population])

    # Gather fitness values on root
    all_fitness = comm.gather(local_fitness, root=0)
    
    if rank == 0:
        fitness = np.concatenate(all_fitness)
        population = list(np.concatenate(comm.gather(local_population, root=0)))

        best_idx = np.argmin(fitness)
        best_ind = population[best_idx]
        best_score = fitness[best_idx]

        print(f"Generation {generation} — Best Fitness: {best_score}")

        selected = select_in_tournament(population, fitness)
        offspring = []
        for i in range(0, len(selected), 2):
            p1, p2 = selected[i], selected[i+1]
            if len(p1[1:]) != len(p2[1:]):
                continue  # Skip malformed pair
            child = [0] + order_crossover(p1[1:], p2[1:])
            offspring.append(mutate(child, mutation_rate))


        for i, idx in enumerate(np.argsort(fitness)[-len(offspring):]):
            population[idx] = offspring[i]

    population = comm.bcast(population, root=0)

if rank == 0:
    print("Final Best Route:", best_ind)
    print("Total Distance:", best_score)
