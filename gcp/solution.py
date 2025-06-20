"""
A Solution object = genome + utility helpers.
"""
from __future__ import annotations
from typing import List, Set
import random
import numpy as np
from .graph import Graph

class Solution:
    def __init__(self, colors: List[int]):
        self.colors = colors

    @classmethod
    def greedy(cls, g: Graph) -> "Solution":
        order = sorted(range(g.n), key=lambda v: len(g.adj[v]), reverse=True)
        colors = [-1] * g.n
        for v in order:
            forbidden = {colors[u] for u in g.adj[v] if colors[u] != -1}
            c = 0
            while c in forbidden:
                c += 1
            colors[v] = c
        return cls(colors)

    # ------------------------------------------------------------------ #
    @classmethod
    def random(cls, g: Graph, max_colors: int) -> "Solution":
        arr = np.random.randint(0, max_colors, size=g.n).tolist()
        return cls(arr)

    # ------------------------------------------------------------------ #
    def fitness(self, g: Graph, penalty: int) -> int:
        conflicts = g.conflict_count(self.colors)
        k_used   = len(set(self.colors))
        return conflicts * penalty + k_used      # lower = better

    def copy(self) -> "Solution":
        return Solution(self.colors.copy())

    # ------------------------------------------------------------------ #
    def kempe_chain_local_search(self, g: Graph) -> None:
        """One Kempe‐chain swap attempt to fix a random conflict."""
        import collections
        # gather all conflicting edges
        bad_edges = [(u, v) for u, v in g.edges if self.colors[u] == self.colors[v]]
        if not bad_edges:
            return
        u, v = random.choice(bad_edges)
        c1, c2 = self.colors[u], self.colors[v]
        # BFS for (c1,c2)-Kempe chain starting at u
        queue = collections.deque([u])
        chain = {u}
        while queue:
            cur = queue.popleft()
            for nb in g.adj[cur]:
                if nb not in chain and self.colors[nb] in (c1, c2):
                    chain.add(nb)
                    queue.append(nb)
        # swap colors in chain
        for idx in chain:
            self.colors[idx] = c2 if self.colors[idx] == c1 else c1
