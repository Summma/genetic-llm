from scipy.special import softmax
import numpy as np

"""
Contains a (function, score) pair.
"""
class Sample:
    def __init__(self, function: str, score: float) -> None:
        self.function: str = function
        self.score: float = score


"""
Each island contains a population of functions that can evolve.
When sampling from an island, a function is chosen based on how good its
score is, and how simple it is.
"""
class Island:
    def __init__(self) -> None:
        self.population = []

    def get_sample(self) -> Sample:
        scores = [sample.score for sample in self.population]
        probs = softmax(scores)
        print(type(probs))
        return Sample("", 1.0)


if __name__ == "__main__":
    island = Island()
    island.population.append(Sample("", 2.0))
    island.population.append(Sample("", 1.0))
    island.population.append(Sample("", -1.0))
    island.population.append(Sample("", -2.0))

    island.get_sample()
