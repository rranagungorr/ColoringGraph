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
        ind = [
            Solution.random(self.g, max_colors=self.g.n)
            for _ in range(self.cfg["population_size"])
        ]
        return Population(ind)

    # ------------------------------------------------------------------ #
    def _adaptive_mut_rate(self, pop_div: float) -> float:
        """Linear schedule between min and max based on diversity."""
        lo, hi = self.cfg["mutation_rate_min"], self.cfg["mutation_rate_max"]
        thr = self.cfg["diversity_threshold"]
        # if diversity <= threshold → use hi, else interpolate down to lo
        if pop_div <= thr:
            return hi
        ratio = (pop_div - thr) / (1 - thr)
        return hi - ratio * (hi - lo)

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
            elite, _ = self.pop.best()
            worst_idx = int(np.argmax([s.fitness(self.g, self.penalty) for s in nxt]))
            nxt[worst_idx] = elite  # keep elite

            self.pop = Population(nxt)

        return stats
