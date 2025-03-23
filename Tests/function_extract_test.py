from utils.models import Ollama
from utils.function_extract import extract_python, extract_given_name

llm = Ollama("deepseek-coder-v2:16b")


prompt = """Make a function that returns either a constant, an index to an operator list, or a an index n for a variable x_n.
The function is meant to be called sequentially to produce a final symbol stack. -1 is return to stop the sequence.
Build this function so that it solves the following differential equation: y'(x0) = 2*x0, y(0) = 1.

For constants, return: (c, 0)
For operators, return: (i, 1)
For variables, return: (n, 2)
For stop, return: (-1, -1)

An example of a possible function might look like this:
def priority(op_list, symbol_stack):
    # op_list: list of available operators to us
    # symbol_stack: the symbol stack in the current iteration

    return (1.2, 0)

which, when called, would constantly tell us to add 1.2 as a constant to the symbol stack.

Change it in a way you think will solve the differential equation better. Only implement the priority() function and nothing else.
"""


response = llm.invoke(prompt)
code = extract_python(response)
func = extract_given_name(code, "priority")

print(func)
