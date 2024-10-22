import numpy as np

from collections import deque
from copy import deepcopy


class Operations:
    @staticmethod
    def add(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return x + y

    @staticmethod
    def subtract(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return x - y

    @staticmethod
    def multiply(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return x * y
    
    @staticmethod
    def divide(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return x / y
    
    @staticmethod
    def pow(x: np.ndarray, y: np.ndarray) -> np.ndarray:
        return np.power(x, y)
    
    @staticmethod
    def sin(x: np.ndarray) -> np.ndarray:
        return np.sin(x)
    
    @staticmethod
    def cos(x: np.ndarray) -> np.ndarray:
        return np.cos(x)
    
    @staticmethod
    def exp(x: np.ndarray) -> np.ndarray:
        return np.exp(x)


class Equation:
    def __init__(self) -> None:
        self.stack: deque[np.ndarray] = deque()
        self.queue: deque[str] = deque()

        self.operation_map = {
            "+": (Operations.add, 2),
            "-": (Operations.subtract, 2),
            "*": (Operations.multiply, 2),
            "/": (Operations.divide, 2),
            "^": (Operations.pow, 2),
            "sin": (Operations.sin, 1),
            "cos": (Operations.cos, 1),
            "exp": (Operations.exp, 1)
        }

    def add_stack(self, operand: np.ndarray):
        self.stack.append(operand)

    def add_queue(self, operation: str):
        self.queue.append(operation)

    def pop_stack(self) -> np.ndarray:
        return self.stack.pop()
    
    def pop_queue(self) -> str:
        return self.queue.popleft()
    
    def evaluate(self, data: np.ndarray = np.array([])) -> np.ndarray | None:
        stack = deepcopy(self.stack)
        queue = deepcopy(self.queue)

        while len(queue) > 0:
            curr = queue.popleft()
            
            if curr.isnumeric():
                stack.append(np.array([float(curr)]))
            elif curr in self.operation_map:
                operation, reps = self.operation_map[curr]
                
                if reps == 2:
                    if len(stack) < 2:
                        print("Incorrect Equation Format")
                        return None

                    first = stack.pop()
                    second = stack.pop()

                    stack.append(operation(first, second))
                elif reps == 1:
                    if len(stack) < 1:
                        print("Incorrect Equation Format")
                        return None
                    
                    first = stack.pop()

                    stack.append(operation(first))
            elif curr[0] == "x" and curr[1:].isnumeric():
                index = int(curr[1:])
                if index < data.shape[1]:
                    stack.append(data[:, index])
            else:
                print("Invalid Character in Equation")
                return None

        return stack.pop()


if __name__ == "__main__":
    equation = Equation()
    string = "4 3 - 5 + sin exp exp x1 * x2 + x0 *"

    for char in string.split():
        equation.add_queue(char)

    print(equation.evaluate(np.array([
        [1, 2, 3],
        [4, 5, 6],
    ])))
