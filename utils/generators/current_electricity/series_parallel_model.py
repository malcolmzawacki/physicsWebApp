from __future__ import annotations

import random

from .ohms_law_model import format_answer_value


SERIES_PARALLEL_PROBLEM_TYPES: tuple[str, ...] = (
    "Series Equivalent Resistance",
    "Series Total Current",
    "Parallel Equivalent Resistance",
    "Parallel Branch Current",
)


SERIES_PARALLEL_MODEL_NOTES = {
    "series_equation": "R_total = R1 + R2",
    "parallel_equation": "1 / R_eq = 1 / R1 + 1 / R2",
    "parallel_voltage": "In parallel, each branch has the same voltage as the source.",
}


def _series_pairs(difficulty: str) -> tuple[tuple[float, float], ...]:
    if difficulty == "Easy":
        return ((2, 4), (3, 5), (4, 6), (5, 7), (6, 8))
    if difficulty == "Medium":
        return ((3, 9), (4, 8), (5, 10), (6, 12), (8, 16))
    return ((2.5, 7.5), (4.0, 10.0), (5.0, 15.0), (6.0, 18.0))


def _parallel_pairs(difficulty: str) -> tuple[tuple[float, float], ...]:
    if difficulty == "Easy":
        return ((6, 3), (4, 4), (6, 6), (8, 8), (12, 6))
    if difficulty == "Medium":
        return ((12, 4), (9, 18), (10, 10), (15, 5), (20, 5))
    return ((7.5, 7.5), (12, 8), (18, 9), (16, 16), (20, 10))


def _build_series_equivalent_case(difficulty: str) -> dict:
    r1, r2 = random.choice(_series_pairs(difficulty))
    answer = r1 + r2
    return {
        "problem_type": "Series Equivalent Resistance",
        "difficulty": difficulty,
        "prompt": "Find the equivalent resistance of the series circuit.",
        "answer": answer,
        "unit": "ohms",
        "givens": (
            ("R1", f"{format_answer_value(r1)} ohms"),
            ("R2", f"{format_answer_value(r2)} ohms"),
        ),
        "diagram": {
            "kind": "series",
            "source_label": "? V",
            "resistor_labels": [f"R1 = {format_answer_value(r1)} ohms", f"R2 = {format_answer_value(r2)} ohms"],
            "wire_label": "",
        },
        "answer_label": "Equivalent resistance",
        "equations": ("`R_total = R1 + R2`",),
        "explanation": (
            f"For a series circuit, resistances add directly: "
            f"{format_answer_value(r1)} ohms + {format_answer_value(r2)} ohms = {format_answer_value(answer)} ohms."
        ),
    }


def _build_series_total_current_case(difficulty: str) -> dict:
    r1, r2 = random.choice(_series_pairs(difficulty))
    if difficulty == "Easy":
        current = random.randint(1, 4)
    elif difficulty == "Medium":
        current = random.choice((0.5, 1.0, 1.5, 2.0, 2.5))
    else:
        current = random.choice((0.6, 0.8, 1.2, 1.5, 2.4))
    total_resistance = r1 + r2
    source_voltage = total_resistance * current
    return {
        "problem_type": "Series Total Current",
        "difficulty": difficulty,
        "prompt": "Find the total current in the series circuit.",
        "answer": current,
        "unit": "A",
        "givens": (
            ("Battery voltage", f"{format_answer_value(source_voltage)} V"),
            ("R1", f"{format_answer_value(r1)} ohms"),
            ("R2", f"{format_answer_value(r2)} ohms"),
        ),
        "diagram": {
            "kind": "series",
            "source_label": f"{format_answer_value(source_voltage)} V",
            "resistor_labels": [f"R1 = {format_answer_value(r1)} ohms", f"R2 = {format_answer_value(r2)} ohms"],
            "wire_label": "I = ? A",
        },
        "answer_label": "Total current",
        "equations": ("`R_total = R1 + R2`", "`I = V / R_total`"),
        "explanation": (
            f"First combine the series resistors: R_total = {format_answer_value(r1)} ohms + "
            f"{format_answer_value(r2)} ohms = {format_answer_value(total_resistance)} ohms. "
            f"Then use I = V / R_total = {format_answer_value(source_voltage)} V / "
            f"{format_answer_value(total_resistance)} ohms = {format_answer_value(current)} A."
        ),
    }


def _build_parallel_equivalent_case(difficulty: str) -> dict:
    r1, r2 = random.choice(_parallel_pairs(difficulty))
    answer = (r1 * r2) / (r1 + r2)
    return {
        "problem_type": "Parallel Equivalent Resistance",
        "difficulty": difficulty,
        "prompt": "Find the equivalent resistance of the two-resistor parallel circuit.",
        "answer": answer,
        "unit": "ohms",
        "givens": (
            ("R1", f"{format_answer_value(r1)} ohms"),
            ("R2", f"{format_answer_value(r2)} ohms"),
        ),
        "diagram": {
            "kind": "parallel",
            "source_label": "? V",
            "resistor_labels": [f"R1 = {format_answer_value(r1)} ohms", f"R2 = {format_answer_value(r2)} ohms"],
            "wire_label": "",
        },
        "answer_label": "Equivalent resistance",
        "equations": ("`1 / R_eq = 1 / R1 + 1 / R2`",),
        "explanation": (
            f"For two resistors in parallel, 1 / R_eq = 1 / {format_answer_value(r1)} + 1 / {format_answer_value(r2)}. "
            f"That gives R_eq = {format_answer_value(answer)} ohms."
        ),
    }


def _build_parallel_branch_current_case(difficulty: str) -> dict:
    r1, r2 = random.choice(_parallel_pairs(difficulty))
    if difficulty == "Easy":
        source_voltage = random.choice((6, 12, 18))
    elif difficulty == "Medium":
        source_voltage = random.choice((9, 12, 15, 18, 20))
    else:
        source_voltage = random.choice((7.5, 12, 16, 18, 24))
    target_index = random.choice((0, 1))
    target_name = f"R{target_index + 1}"
    target_resistance = (r1, r2)[target_index]
    answer = source_voltage / target_resistance
    return {
        "problem_type": "Parallel Branch Current",
        "difficulty": difficulty,
        "prompt": f"Find the current through branch {target_name}.",
        "answer": answer,
        "unit": "A",
        "givens": (
            ("Battery voltage", f"{format_answer_value(source_voltage)} V"),
            ("R1", f"{format_answer_value(r1)} ohms"),
            ("R2", f"{format_answer_value(r2)} ohms"),
        ),
        "diagram": {
            "kind": "parallel",
            "source_label": f"{format_answer_value(source_voltage)} V",
            "resistor_labels": [f"R1 = {format_answer_value(r1)} ohms", f"R2 = {format_answer_value(r2)} ohms"],
            "wire_label": "",
        },
        "answer_label": f"Current through {target_name}",
        "equations": ("`V_branch = V_source`", "`I = V / R`"),
        "explanation": (
            f"In parallel, each branch gets the full source voltage, so {target_name} has "
            f"{format_answer_value(source_voltage)} V across it. Then use I = V / R: "
            f"{format_answer_value(source_voltage)} V / {format_answer_value(target_resistance)} ohms = "
            f"{format_answer_value(answer)} A."
        ),
    }


def build_series_parallel_case(problem_type: str, difficulty: str) -> dict:
    if problem_type == "Series Equivalent Resistance":
        return _build_series_equivalent_case(difficulty)
    if problem_type == "Series Total Current":
        return _build_series_total_current_case(difficulty)
    if problem_type == "Parallel Equivalent Resistance":
        return _build_parallel_equivalent_case(difficulty)
    if problem_type == "Parallel Branch Current":
        return _build_parallel_branch_current_case(difficulty)
    raise ValueError(f"Unsupported series/parallel problem type: {problem_type}")
