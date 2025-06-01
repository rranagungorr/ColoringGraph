"""
Graph reader and lightweight adjacency structure for DIMACS‐like TXT files.
File format:
    first line : <n_vertices> <n_edges>
    next m lines: <u> <v>   (0-based vertex indices)
"""
from typing import List

class Graph:
    def __init__(self, path: str):
        self.n = 0                # vertex count
        self.edges: List[tuple] = []
        self.adj:  List[List[int]] = []
        self._read(path)

    # ------------------------------------------------------------------ #
    def _read(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            header = f.readline().split()
            self.n, m = map(int, header)
            self.adj = [[] for _ in range(self.n)]
            for _ in range(m):
                u, v = map(int, f.readline().split())
                self.edges.append((u, v))
                self.adj[u].append(v)
                self.adj[v].append(u)

    # ------------------------------------------------------------------ #
    def conflict_count(self, coloring) -> int:
        """Return number of edges whose endpoints share the same color."""
        return sum(coloring[u] == coloring[v] for u, v in self.edges)
