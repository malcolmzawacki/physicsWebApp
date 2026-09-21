"""Explicit grading policies shared by activity layouts."""
import math

STANDARD_POLICY = {"rel_tol": 0.1, "abs_tol": 1e-9}
CIRCUIT_POLICY = {"rel_tol": 0.05, "abs_tol": 0.05}
DIFFICULTY_STARS = {"Easy": 1, "Medium": 2, "Hard": 3}


def parse_number(value):
    number = float(str(value).strip())
    if not math.isfinite(number):
        raise ValueError("Enter a finite number.")
    return number


def answer_matches(value, expected, policy=None):
    if isinstance(expected, str):
        return str(value).strip().casefold() == expected.strip().casefold()
    policy = STANDARD_POLICY if policy is None else policy
    number = parse_number(value)
    # Tolerance is based on the expected value, not on the student's value.
    tolerance = max(abs(expected) * policy["rel_tol"], policy["abs_tol"])
    return abs(number - expected) <= tolerance
