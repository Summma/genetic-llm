from utils.models import Ollama

llm = Ollama("deepseek-coder-v2:16b")

prompt = """You are given only the numpy library. Given multidimensional input, output a set of functions that could possibly be used to 
represent the given input. For example, the input could be of the positions of particles at a certain time. The output would be a list of
possible elementary functions that could be used to model the physical scenarion. For example, given a specific (x, y, z, t), your function
should output a list of elementary functions like [sin, cos, sin(x)e^t] that could be combined to output a temperature T. Make this function in Python
using nothing but numpy. Do this by manipulating the data in a way that allows you to figure out these functions."""

"""
1. Have LLM generate function to build the syntax tree
2. Evaluate the results of the syntax tree
    2a. Maybe incorporate some of the PINN stuff.
3. Insert the prompt and results into the pool of islands
4. Do genetic evolution stuff

"""

print(llm.invoke(prompt))
