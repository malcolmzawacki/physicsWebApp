"""Small scientific calculator with a deliberately restricted expression grammar."""

import ast
import math
import operator


def calculate(expression: str, degrees: bool = True, answer: float = 0) -> float:
    """Evaluate real arithmetic without executing Python or accepting attributes."""
    if len(expression) > 250:
        raise ValueError("Please use an expression of 250 characters or fewer.")
    source = expression.strip().replace("×", "*").replace("÷", "/").replace("−", "-").replace("^", "**")
    operators = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
                 ast.Div: operator.truediv, ast.Pow: operator.pow}
    angle = math.radians if degrees else float
    inverse_angle = math.degrees if degrees else float
    functions = {"sqrt": math.sqrt, "sin": lambda x: math.sin(angle(x)),
                 "cos": lambda x: math.cos(angle(x)), "tan": lambda x: math.tan(angle(x)),
                 "asin": lambda x: inverse_angle(math.asin(x)),
                 "acos": lambda x: inverse_angle(math.acos(x)),
                 "atan": lambda x: inverse_angle(math.atan(x)),
                 "log": math.log10, "ln": math.log, "abs": abs}
    constants = {"pi": math.pi, "e": math.e, "ans": answer}

    def bounded(value):
        if isinstance(value, complex) or not math.isfinite(value):
            raise ValueError("The result must be a finite real number.")
        return float(value)

    def visit(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return bounded(node.value)
        if isinstance(node, ast.Name) and node.id in constants:
            return bounded(constants[node.id])
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.BinOp) and type(node.op) in operators:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 1000:
                raise ValueError("Please use an exponent between -1000 and 1000.")
            return bounded(operators[type(node.op)](left, right))
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in functions and len(node.args) == 1 and not node.keywords):
            return bounded(functions[node.func.id](visit(node.args[0])))
        raise ValueError("Use numbers, arithmetic, parentheses, or a listed function.")

    try:
        return visit(ast.parse(source, mode="eval").body)
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero.") from None
    except (SyntaxError, TypeError):
        raise ValueError("Check the expression and close any parentheses. Use * for multiplication.") from None
    except (OverflowError, RecursionError):
        raise ValueError("That calculation is too large or too deeply nested.") from None
    except ValueError as exc:
        if str(exc) == "math domain error":
            raise ValueError("That function is outside its real-number domain.") from None
        raise
