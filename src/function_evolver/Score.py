from copy import deepcopy
from typing import Callable

import sympy
from pysr import PySRRegressor # type: ignore

from src.function_evolver.SymbolStack import Equation


def build_symbolic_regression(
    func: str,
    name: str,
    binary_operators: list[str],
    unary_operators: list[str],
    extra_sympy_mappings: dict[str, Callable] = {}
) -> PySRRegressor:
    vars = {}
    exec(f"{func}", {}, vars)
    priority_function: Callable = vars[name]
    binary_weights = [0] * len(binary_operators)
    unary_weights = [0] * len(unary_operators)

    for i in range(len(binary_operators)):
        priority = priority_function(binary_operators, binary_operators[i])
        binary_weights[i % len(binary_operators)] = priority

    for i in range(len(unary_operators)):
        priority = priority_function(unary_operators, unary_operators[i])
        unary_weights[i % len(unary_operators)] = priority

    normalize = lambda x: [(a + 0.01) / (sum(x) + len(x) * 0.01) for a in x]

    binary_weights = normalize(binary_weights)
    unary_weights = normalize(unary_weights)

    print(binary_operators, binary_weights)
    print(unary_operators, unary_weights)

    model = PySRRegressor(
        model_selection="best",  # Result is mix of simplicity+accuracy
        niterations=40,
        binary_operators=binary_operators,
        unary_operators=unary_operators,
        extra_sympy_mappings={"inv": lambda x: 1 / x, "both": lambda x: (sympy.Integer(2) * sympy.cos(x) * sympy.sin(x))},
        # ^ Define operator for SymPy as well
        elementwise_loss="loss(x, y) = (x - y)^2",
        # ^ Custom loss function (julia syntax)
        bin_op_weight=binary_weights,
        un_op_weight=unary_weights,
        turbo=True,
        verbosity=0,
    )

    return model


def build_stack(func: str, name: str) -> Equation:
    num, _type = 0, 0
    symbol_stack = Equation()

    fail_safe = 100
    while fail_safe >= 0:
        vars = {}
        exec(f"{func}", {}, vars)
        priority: Callable = vars[name]

        num, _type = priority(symbol_stack.queue)
        print(symbol_stack.queue)

        match (_type, num):
            case (0, num):
                symbol_stack.add_queue(str(num))

            case (1, num):
                symbol_stack.add_queue(list(symbol_stack.operation_map.keys())[num])

            case (2, num):
                symbol_stack.add_queue(f"x{num}")

            case (-1, num):
                break

            case _:
                print("Weird behavior")


        fail_safe -= 1
    else:
        print("Potential infinite loop")

    return symbol_stack


if __name__ == "__main__":
    build_stack("def priority(b, c):\n    return (4.2, b)", "a")
