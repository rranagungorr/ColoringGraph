
import random
from src.utils import fitness

def generate_individual(num_nodes, max_colors):
    return [random.randint(0, max_colors - 1) for _ in range(num_nodes)]

def mutate(individual, max_colors):
    child = individual[:]
    idx = random.randint(0, len(child) - 1)
    child[idx] = random.randint(0, max_colors - 1)
    return child

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 2)
    return parent1[:point] + parent2[point:]

def run_ga(num_nodes, edges, population_size=100, generations=1000, max_colors=20):
    population = [generate_individual(num_nodes, max_colors) for _ in range(population_size)]

    for gen in range(generations):
        scored = [(ind, fitness(ind, edges)) for ind in population]
        scored.sort(key=lambda x: x[1])
        population = [ind for ind, score in scored[:10]]  # elitism

        while len(population) < population_size:
            parent1, parent2 = random.sample(population[:50], 2)
            child = crossover(parent1, parent2)
            child = mutate(child, max_colors)
            population.append(child)

        if gen % 100 == 0:
            print(f"Generation {gen} - Best Fitness: {scored[0][1]}")

    best = min(population, key=lambda ind: fitness(ind, edges))
    return best
