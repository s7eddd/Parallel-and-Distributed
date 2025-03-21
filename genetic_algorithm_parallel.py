from mpi4py import MPI
import numpy as np
import pandas as pd
from genetic_algorithms_functions import (
    calculate_fitness,
    select_in_tournament,
    order_crossover,
    mutate,
    generate_unique_population
)

# -------------------------------------
# MPI Initialization
# -------------------------------------
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
world_size = comm.Get_size()

# -------------------------------------
# Configuration Parameters
# -------------------------------------
distance_data = pd.read_csv("city_distances.csv").to_numpy()
num_cities = distance_data.shape[0]
pop_size = 10000
generations = 200
mutation_chance = 0.1
max_stagnant_generations = 5

# -------------------------------------
# Validity Checker for Routes
# -------------------------------------
def route_is_valid(route):
    for i in range(len(route) - 1):
        if distance_data[route[i], route[i + 1]] >= 100000:
            return False
    if distance_data[route[-1], route[0]] >= 100000:
        return False
    return True

# -------------------------------------
# Population Initialization by Root
# -------------------------------------
if rank == 0:
    initial_population = generate_unique_population(pop_size, num_cities)
else:
    initial_population = None

# Share initial population with all processes
initial_population = comm.bcast(initial_population, root=0)

# -------------------------------------
# Genetic Algorithm Evolution Loop
# -------------------------------------
best_score = float('inf')
stagnant_gen = 0

for gen in range(generations):
    refreshed = False

    segment_sizes = [len(initial_population) // world_size + (1 if i < len(initial_population) % world_size else 0) for i in range(world_size)]
    segment_starts = [sum(segment_sizes[:i]) for i in range(world_size)]
    local_segment = initial_population[segment_starts[rank]:segment_starts[rank] + segment_sizes[rank]]

    local_scores = np.array([calculate_fitness(indiv, distance_data) for indiv in local_segment])

    collected_scores = None
    if rank == 0:
        collected_scores = np.empty(len(initial_population), dtype=np.float64)

    recv_counts = np.array(segment_sizes, dtype=int)
    displs = np.array(segment_starts, dtype=int)

    comm.Gatherv(local_scores, [collected_scores, recv_counts, displs, MPI.DOUBLE], root=0)

    if rank == 0:
        current_min = np.min(collected_scores)  # Fix: use min instead of max

        if current_min < best_score or gen == 0:
            best_score = current_min
            stagnant_gen = 0
        else:
            stagnant_gen += 1

        if stagnant_gen >= max_stagnant_generations:
            print(f"[Gen {gen}] Stagnation detected. Regenerating population...", flush=True)
            elite_indices = np.argsort(collected_scores)[:10]  # Fix: select best 10
            elite_individuals = [initial_population[i] for i in elite_indices]
            new_population = generate_unique_population(pop_size - len(elite_individuals), num_cities)
            new_population.extend(elite_individuals)
            initial_population = new_population
            stagnant_gen = 0
            refreshed = True

    initial_population = comm.bcast(initial_population, root=0)
    refreshed = comm.bcast(refreshed if rank == 0 else None, root=0)

    if refreshed:
        continue

    # -------------------------------------
    # Breeding & Mutation by Root
    # -------------------------------------
    if rank == 0:
        selected_individuals = select_in_tournament(initial_population, collected_scores)
        np.random.shuffle(selected_individuals)

        children = []
        for i in range(0, len(selected_individuals), 2):
            p1, p2 = selected_individuals[i], selected_individuals[i + 1]
            offspring = order_crossover(p1[1:], p2[1:])
            mutated_offspring = mutate([0] + offspring, mutation_chance)

            if route_is_valid(mutated_offspring):  # Fix: Ensure route validity
                children.append(mutated_offspring)

        initial_population = children

        print(f"Generation {gen} | Best Score: {current_min:.2f} | Worst: {np.max(collected_scores):.2f}", flush=True)

    initial_population = comm.bcast(initial_population, root=0)

# -------------------------------------
# Final Output by Root
# -------------------------------------
if rank == 0:
    final_scores = np.array([calculate_fitness(indiv, distance_data) for indiv in initial_population])
    best_index = np.argmin(final_scores)  # Fix: use argmin
    optimal_route = initial_population[best_index]
    print("\nOptimal Route Found:", optimal_route, flush=True)
    print("Minimum Distance:", final_scores[best_index], flush=True)
