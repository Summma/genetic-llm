import numpy as np
import sympy
import matplotlib.pyplot as plt

from time import time

X = 2 * np.random.randn(100, 5)
y = 2.5382 * np.sin(X[:, 3]) + X[:, 0] ** 2 - 0.5

from pysr import PySRRegressor

model = PySRRegressor(
    model_selection="best",  # Result is mix of simplicity+accuracy
    niterations=40,
    binary_operators=["+", "*"],
    unary_operators=[
        "cos",
        "exp",
        "inv(x) = 1/x",
        "both(x) = 2 * cos(x) * sin(x)",
        # ^ Custom operator (julia syntax)
    ],
    extra_sympy_mappings={"inv": lambda x: 1 / x, "both": lambda x: (2 * sympy.cos(x) * sympy.sin(x))},
    # ^ Define operator for SymPy as well
    elementwise_loss="loss(x, y) = (x - y)^2",
    # ^ Custom loss function (julia syntax)
    bin_op_weight=[0.5, 0.5],
    un_op_weight=[0, 0.15, 0.15, 0.7],
    turbo=True,
)

start = time()
model.fit(X, y)

print(model.predict(X) - y)

print(time() - start)
