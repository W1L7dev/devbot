import math
import string
from typing import List


def solve_expr(expr: str):
    """Solves a math expression

    Args:
        expr (str): The math expression

    Returns:
        str: The result of the math expression
    """
    operators = {
        "^": math.pow,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
        "%": lambda x, y: x % y,
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
    }
    tokens = []
    token = ""
    for char in expr:
        if char in string.whitespace:
            continue
        elif char in operators.keys() or char in "()":
            if token != "":
                tokens.append(token)
                token = ""
            tokens.append(char)
        else:
            token += char
    if token != "":
        tokens.append(token)
    while "(" in tokens:
        start = 0
        end = len(tokens)
        for i, token in enumerate(tokens):
            if token == "(":
                start = i
            elif token == ")":
                end = i
                break
        expr = tokens[start + 1 : end]
        result = solve_expr(" ".join(expr))
        tokens = tokens[:start] + [result] + tokens[end + 1 :]
    for op in "^*/%+-":
        while op in tokens:
            idx = tokens.index(op)
            left = float(tokens[idx - 1])
            right = float(tokens[idx + 1])
            result = operators[op](left, right)
            tokens = tokens[: idx - 1] + [result] + tokens[idx + 2 :]

    return str(tokens[0])
