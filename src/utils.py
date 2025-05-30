def fitness(individual, edges):
    penalty = 0
    for u, v in edges:
        if individual[u] == individual[v]:
            penalty += 1
    return len(set(individual)) + penalty * 10  # cezalı fitness
