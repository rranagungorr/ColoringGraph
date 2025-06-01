import random
from typing import List

def tournament(pop: List, fitnesses: List[int], k: int) -> int:
    """Return index of winner among k random contenders."""
    best = random.choice(range(len(pop)))
    for _ in range(k - 1):
        challenger = random.choice(range(len(pop)))
        if fitnesses[challenger] < fitnesses[best]:
            best = challenger
    return best
