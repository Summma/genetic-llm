import ast

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


if __name__ == "__main__":
    code = "def test():\n\tprint(123)"
    try:
        exec(f"{extract(code)}\ntest()")
    except NameError:
        print("Function not defined correctly")

    code_two = "def kasjdlajskjdklasjdk():\n\tprint(456)"
    body, name = extract_with_name(code_two)
    exec(f"{body}\n{name}()")
