from scipy.special import softmax
import numpy as np

from dataclasses import dataclass

"""
Contains a (function, score) pair.
"""
@dataclass
class Sample:
    function: str = ""
    score: float = 0

    def __repr__(self) -> str:
        return str(self.score)


"""
Each island contains a population of functions that can evolve.
When sampling from an island, a function is chosen based on how good its
score is, and how simple it is.
"""
class Island:
    def __init__(self) -> None:
        self.population: list[Sample] = []
        self.best_sample: Sample = Sample()
        self.size: int = 0

    def get_sample(self) -> Sample:
        scores = [sample.score for sample in self.population]
        probs = softmax(scores)

        index = np.random.choice(self.size, 1, p=probs)[0]
        sample = self.population[index]

        return sample
    
    def get_uniform_random_sample(self) -> Sample:
        index = np.random.choice(self.size, 1)[0]
        sample = self.population[index]

        return sample
    
    def add_sample(self, sample: Sample) -> None:
        self.population.append(sample)
        self.best_sample = max(self.best_sample, sample, key=lambda x: x.score)
        self.size += 1

    def reset_population(self) -> None:
        self.population = []
        self.best_sample = Sample()
        self.size = 0

    def __repr__(self) -> str:
        return str(self.population)


if __name__ == "__main__":
    island = Island()
    island.population.append(Sample("", 2.0))
    island.population.append(Sample("", 1.0))
    island.population.append(Sample("", -1.0))
    island.population.append(Sample("", -2.0))

    print(island.get_sample())
    print(island.get_sample())
    print(island.get_sample())
    print(island.get_sample())
