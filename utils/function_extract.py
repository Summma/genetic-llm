import ast
import re

def extract(code: str) -> str:
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            return ast.unparse(node)

    return ""


def extract_with_name(code: str) -> tuple[str, str]:
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            return (ast.unparse(node), node.name)

    return ("", "")


def extract_given_name(code: str, name: str) -> str:
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == name:
            return ast.unparse(node)

    return ""


def extract_python(md: str) -> str:
    pattern = r"```python\n([\s\S]*)```"
    return re.findall(pattern, md)[0]


if __name__ == "__main__":
    markdown = """
    ```python
print("Hello world")
print("What")
    ```
    """

    code = "def test():\n\tprint(123)"
    try:
        exec(f"{extract(code)}\ntest()")
    except NameError:
        print("Function not defined correctly")

    code_two = "def kasjdlajskjdklasjdk():\n\tprint(456)"
    body, name = extract_with_name(code_two)
    exec(f"{body}\n{name}()")

    exec(extract_python(markdown))
