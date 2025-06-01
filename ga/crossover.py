import random
from typing import List, Tuple

def uniform(parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
    """50/50 gene mixing."""
    child1, child2 = parent1.copy(), parent2.copy()
    for i in range(len(parent1)):
        if random.random() < 0.5:
            child1[i], child2[i] = child2[i], child1[i]
    return child1, child2
