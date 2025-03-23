import numpy as np

def calculate_fitness(route, distance_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        dist = distance_matrix[route[i]][route[i + 1]]
        if dist >= 100000:
            return 1e6
        total_distance += dist
    dist = distance_matrix[route[-1]][route[0]]
    if dist >= 100000:
        return 1e6
    total_distance += dist
    return total_distance

def select_in_tournament(population, scores, number_tournaments=4, tournament_size=3):
    selected = []
    for _ in range(len(population) // 2):
        idx = np.random.choice(len(population), tournament_size, replace=False)
        best_idx = idx[np.argmin(scores[idx])]
        selected.append(population[best_idx])
        idx = np.random.choice(len(population), tournament_size, replace=False)
        best_idx = idx[np.argmin(scores[idx])]
        selected.append(population[best_idx])
    return selected

def order_crossover(parent1, parent2):
    size = len(parent1)
    if len(parent1) != len(parent2):
        raise ValueError("Parents must be of the same length")

    start, end = sorted(np.random.choice(range(size), 2, replace=False))
    offspring = [None] * size
    offspring[start:end + 1] = parent1[start:end + 1]
    fill_values = [x for x in parent2 if x not in offspring[start:end + 1]]
    idx = 0
    for i in range(size):
        if offspring[i] is None:
            if idx >= len(fill_values):  # Defensive fix
                raise IndexError("Not enough fill values in crossover")
            offspring[i] = fill_values[idx]
            idx += 1
    return offspring


def mutate(route, mutation_rate=0.1):
    if np.random.rand() < mutation_rate:
        i, j = np.random.choice(len(route), 2, replace=False)
        route[i], route[j] = route[j], route[i]
    return route

def generate_unique_population(population_size, num_nodes):
    population = set()
    while len(population) < population_size:
        individual = [0] + list(np.random.permutation(np.arange(1, num_nodes)))
        population.add(tuple(individual))
    return [list(ind) for ind in population]
