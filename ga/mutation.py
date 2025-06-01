import random
from typing import List

def mutate(genome: List[int], rate: float, n_colors: int) -> None:
    """Each gene flips to a random color with probability = rate."""
    for i in range(len(genome)):
        if random.random() < rate:
            genome[i] = random.randint(0, n_colors - 1)
