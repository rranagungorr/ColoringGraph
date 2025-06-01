from typing import List, Tuple
import numpy as np
from gcp.solution import Solution
from gcp.graph import Graph

class Population:
    def __init__(self, individuals: List[Solution]):
        self.individuals = individuals
        self.fitness_cache = None

    # ------------------------------------------------------------------ #
    def evaluate(self, g: Graph, penalty: int) -> List[int]:
        """Compute & memoize fitness array."""
        self.fitness_cache = [sol.fitness(g, penalty) for sol in self.individuals]
        return self.fitness_cache

    # ------------------------------------------------------------------ #
    def best(self) -> Tuple[Solution, int]:
        idx = int(np.argmin(self.fitness_cache))
        return self.individuals[idx], self.fitness_cache[idx]

    # ------------------------------------------------------------------ #
    def diversity(self) -> float:
        """Fraction of unique genomes."""
        uniq = {tuple(sol.colors) for sol in self.individuals}
        return len(uniq) / len(self.individuals)
