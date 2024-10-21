import time
import random

import numpy as np
from scipy.special import softmax

from src.Island import Island, Sample


"""
This defines an island pool which contains many islands.
Each island runs genetic evolution separateley.
"""
class IslandPool:
    def __init__(
        self, 
        num_islands: int, 
        migration_period: int, 
        migration_rate: int,
        island_reset_rate: float,
    ) -> None:
        self.islands: list[Island] = [Island() for _ in range(num_islands)]
        self.num_islands: int = num_islands
        self.populated_islands: set = set()

        self.island_reset_rate: float = island_reset_rate
        self.last_reset: float = time.time()

        self.migration_period: int = migration_period
        self.migration_rate: int = migration_rate
        self.migration_counter: int = 0

    def add_sample(self, function: str, score: float) -> None:
        # Add sample to island with least population priority

        probs = softmax([-island.size for island in self.islands])
        index = np.random.choice(self.num_islands, 1, p=probs)[0]

        self.populated_islands.add(index)

        self.islands[index].add_sample(Sample(function, score))

        self.migration_counter += 1
        if self.migration_counter >= self.migration_period:
            self.perform_island_migrations()

        if self.last_reset + self.island_reset_rate <= time.time():
            self.reset_islands()
    
    def get_sample(self) -> Sample:
        index = np.random.choice(list(self.populated_islands), 1)[0]
        return self.islands[index].get_sample()

    def reset_islands(self) -> None:
        # Reset the worse half of the islands while leaving the best sample

        sorted_islands_with_index = sorted(enumerate(self.islands), key=lambda x: x[1].best_sample.score)
        
        for index, island in sorted_islands_with_index[:self.num_islands//2]:
            best_sample = island.best_sample
            island.reset_population()
            island.add_sample(best_sample)
            self.populated_islands.remove(index)

        self.last_reset = time.time()

    def perform_island_migrations(self) -> None:
        # Perform many island migrations equal to migration_rate

        if len(self.populated_islands) != self.num_islands:
            return
        
        for _ in range(self.migration_rate):
            self._migrate_random_island()

        self.migration_counter = 0

    def _migrate_random_island(self) -> None:
        # Perform one random migration

        index_from = np.random.choice(self.num_islands, 1)[0]
        index_to = np.random.choice(self.num_islands, 1)[0]

        while index_to == index_from:
            index_to = np.random.choice(self.num_islands, 1)[0]

        sample = self.islands[index_from].get_uniform_random_sample()
        self.islands[index_to].add_sample(sample)


if __name__ == "__main__":
    # Test code to show small improvements to sample has
    # potential to converge.

    island_pool = IslandPool(20, 2, 0, 0.5)

    for i in range(400):
        if i <= 10:
            island_pool.add_sample("sadkj", random.uniform(0, 100))
        else:
            sample = island_pool.get_sample()
            island_pool.add_sample("sadkj", random.uniform(sample.score / 2, 100))

        time.sleep(0.01)

    # For all intents and purposes this is a good enough mean for now
    means = [sum(map(lambda x: x.score, a.population))/a.size for a in island_pool.islands]
    print(sum(means) / len(means))
