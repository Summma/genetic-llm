import matplotlib.pyplot as plt


class Result:
    def __init__(self):
        """Initialize a Result object."""

        self.scores: list[float] = []

    def record_score(self, loss: float):
        """Record the score for the current generation."""
        self.scores.append(loss)

    def plot_scores(self):
        """Plot the recorded scores over generations."""

        plt.plot(self.scores)
        plt.xlabel('Generation')
        plt.ylabel('Loss')
        plt.title('Loss over Generations')
        plt.show()
