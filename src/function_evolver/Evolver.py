import traceback

import numpy as np

from src.function_evolver.IslandPool import IslandPool
from src.function_evolver.Score import build_stack, build_symbolic_regression
from src.function_evolver.Result import Result

from utils.models import Ollama
from utils.function_extract import extract_python, extract_given_name
from utils.prompt import Prompt

class Evolver:
    def __init__(
        self,
        island_pool: IslandPool,
        prompt_file: str,
    ) -> None:
        self.island_pool = island_pool

        self.llm = Ollama("deepseek-coder-v2:16b")
        self.prompt = Prompt(prompt_file)
        self.results: Result = Result()

    def _evaluation_step(self, prompt: str):
        response = self.llm.invoke(self.prompt.prompt)

        try:
            code = extract_python(response)
            func = extract_given_name(code, "priority")

            # print(func)
            # print(build_stack(func, "priority").evaluate())

            L = 1
            C = 1

            X = np.random.rand(100, 2) * 4 - 2
            y = C * np.sinh(np.pi / L * X[:, 0]) * np.exp(-np.pi / L * X[:, 1])

            print("Building model...")
            model = build_symbolic_regression(func, "priority", ["+", "-", "*", "/"], ["sin", "cos", "exp"])
            model.fit(X, y)

            y_hat = model.predict(X)
            loss = np.mean((y - y_hat)**2)

        except Exception as e:
            print(response)
            print(e)
            return "", 0.001

        return func, loss


    def run(self) -> None:
        """
        Runs the evolution process.
        """

        for i in range(40):
            if len(self.island_pool.populated_islands) != self.island_pool.num_islands:
                func, loss = self._evaluation_step(self.prompt.prompt)
                self.island_pool.add_sample(func, loss)
            else:
                print("Database Sampling")
                sample, index = self.island_pool.get_sample()

                prompt, _, _ = self.prompt.substitute_function(sample.function)

                func, loss = self._evaluation_step(prompt)

                self.island_pool.add_sample(func, loss, index)

            print(f"Iteration {i}: Loss {loss:.4f}")

            self.results.record_score(1000 / loss)

        self.results.plot_scores()


if __name__ == "__main__":
    island_pool = IslandPool(20, 2, 10, 10)
    evolver = Evolver(island_pool, "symbolic_prompt.txt")
    evolver.run()
