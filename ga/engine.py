"""
Main GA loop with:
  • tournament selection
  • uniform crossover
  • adaptive mutation
  • Kempe-chain local search
  • elitism
"""
from typing import List
import random
import yaml
import numpy as np
from tqdm import trange

from gcp.graph import Graph
from gcp.solution import Solution
from .selection import tournament
from .crossover import uniform
from .mutation import mutate
from .population import Population


class GAEngine:
    def __init__(self, g: Graph, cfg: dict):
        self.g = g
        self.cfg = cfg
        self.penalty = cfg.get("conflict_penalty", g.n)
        self.pop = self._init_population()

    # ------------------------------------------------------------------ #
    def _init_population(self) -> Population:
        ind = [Solution.greedy(self.g)]
        ind += [Solution.random(self.g, max_colors=self.g.n // 3)
                for _ in range(self.cfg["population_size"] - 1)]
        return Population(ind)

    # ------------------------------------------------------------------ #
    def _adaptive_mut_rate(self, pop_div: float) -> float:
        """Linear schedule between min and max based on diversity."""
        lo, hi = self.cfg["mutation_rate_min"], self.cfg["mutation_rate_max"]
        thr = self.cfg["diversity_threshold"]
        if pop_div >= thr:
            return hi
        ratio = pop_div / thr
        return lo + (hi - lo) * ratio


        # ------------------------------------------------------------------ #
    def run(self) -> dict:
        stats = {"best_fit": [], "avg_fit": []}
        generations = self.cfg["generations"]
        tournament_k = self.cfg["tournament_size"]

        for _ in trange(generations, desc="GA"):
            fits = self.pop.evaluate(self.g, self.penalty)
            best_fit = min(fits)
            stats["best_fit"].append(best_fit)
            stats["avg_fit"].append(float(np.mean(fits)))

            # ---------------- selection ---------------- #
            mating_pool = []
            while len(mating_pool) < len(self.pop.individuals):
                idx = tournament(self.pop.individuals, fits, tournament_k)
                mating_pool.append(self.pop.individuals[idx])

            # ---------------- variation ---------------- #
            nxt = []
            mut_rate = self._adaptive_mut_rate(self.pop.diversity())
            for i in range(0, len(mating_pool), 2):
                p1 = mating_pool[i].colors
                p2 = mating_pool[i + 1].colors
                c1, c2 = uniform(p1, p2)

                mutate(c1, mut_rate, self.g.n)
                mutate(c2, mut_rate, self.g.n)

                child1, child2 = Solution(c1), Solution(c2)
                child1.kempe_chain_local_search(self.g)
                child2.kempe_chain_local_search(self.g)
                nxt.extend([child1, child2])

            # ---------------- elitism ---------------- #
            k = self.cfg.get("elitism_count", 1)

            elite_indices = np.argsort(fits)[:k]
            elites = [self.pop.individuals[i].copy() for i in elite_indices]

            offspring_fits = [s.fitness(self.g, self.penalty) for s in nxt]
            worst_indices = np.argsort(offspring_fits)[-k:]

            for e, w_idx in zip(elites, worst_indices):
                nxt[w_idx] = e

        return stats
