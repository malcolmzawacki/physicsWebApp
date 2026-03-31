from __future__ import annotations

import random


PROBLEM_TYPES: tuple[str, ...] = (
    "Single Resistor",
    "Series Current",
    "Voltage Drop",
)


CIRCUIT_MODEL_NOTES = {
    "scope": (
        "This starter activity uses ideal batteries, ideal wires, and resistors that obey Ohm's law."
    ),
    "current": (
        "In a simple series circuit, the same current passes through each resistor."
    ),
    "series": (
        "For series circuits, total resistance is the sum of the resistor values."
    ),
}


def format_answer_value(value: float) -> str:
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _build_single_resistor_case(difficulty: str) -> dict:
    if difficulty == "Easy":
        resistance = random.randint(2, 12)
        current = random.randint(1, 6)
    elif difficulty == "Medium":
        resistance = random.choice((3, 4, 5, 6, 8, 10, 12, 15, 18))
        current = random.choice((0.5, 1.0, 1.5, 2.0, 2.5, 3.0))
    else:
        resistance = random.choice((2.5, 4.0, 6.0, 7.5, 12.0, 15.0, 18.0))
        current = random.choice((0.4, 0.6, 0.8, 1.2, 1.5, 2.4, 3.2))

    voltage = resistance * current
    solve_for = random.choice(("Voltage", "Current", "Resistance"))

    diagram = {
        "kind": "single",
        "source_label": f"{format_answer_value(voltage)} V" if solve_for != "Voltage" else "? V",
        "resistor_labels": [f"{format_answer_value(resistance)} ohms" if solve_for != "Resistance" else "? ohms"],
        "wire_label": f"I = {format_answer_value(current)} A" if solve_for != "Current" else "I = ? A",
    }

    if solve_for == "Voltage":
        prompt = "Use Ohm's law to calculate the battery voltage."
        answer = voltage
        unit = "V"
        givens = (
            ("Resistance", f"{format_answer_value(resistance)} ohms"),
            ("Current", f"{format_answer_value(current)} A"),
        )
        explanation = (
            f"Use V = IR. With I = {format_answer_value(current)} A and "
            f"R = {format_answer_value(resistance)} ohms, the voltage is {format_answer_value(voltage)} V."
        )
    elif solve_for == "Current":
        prompt = "Use Ohm's law to calculate the current in the circuit."
        answer = current
        unit = "A"
        givens = (
            ("Battery voltage", f"{format_answer_value(voltage)} V"),
            ("Resistance", f"{format_answer_value(resistance)} ohms"),
        )
        explanation = (
            f"Use I = V / R. With V = {format_answer_value(voltage)} V and "
            f"R = {format_answer_value(resistance)} ohms, the current is {format_answer_value(current)} A."
        )
    else:
        prompt = "Use Ohm's law to calculate the resistance of the resistor."
        answer = resistance
        unit = "ohms"
        givens = (
            ("Battery voltage", f"{format_answer_value(voltage)} V"),
            ("Current", f"{format_answer_value(current)} A"),
        )
        explanation = (
            f"Use R = V / I. With V = {format_answer_value(voltage)} V and "
            f"I = {format_answer_value(current)} A, the resistance is {format_answer_value(resistance)} ohms."
        )

    return {
        "problem_type": "Single Resistor",
        "difficulty": difficulty,
        "prompt": prompt,
        "answer": answer,
        "unit": unit,
        "givens": givens,
        "diagram": diagram,
        "answer_label": solve_for,
        "explanation": explanation,
    }


def _build_series_current_case(difficulty: str) -> dict:
    if difficulty == "Easy":
        resistance_pairs = ((2, 4), (3, 5), (4, 6), (5, 7), (6, 8))
        current = random.randint(1, 4)
    elif difficulty == "Medium":
        resistance_pairs = ((3, 9), (4, 8), (5, 10), (6, 12), (8, 16))
        current = random.choice((0.5, 1.0, 1.5, 2.0, 2.5))
    else:
        resistance_pairs = ((2.5, 7.5), (4.0, 10.0), (5.0, 15.0), (6.0, 18.0))
        current = random.choice((0.6, 0.8, 1.2, 1.5, 2.4))

    r1, r2 = random.choice(resistance_pairs)
    total_resistance = r1 + r2
    source_voltage = total_resistance * current
    ask_total_resistance = difficulty == "Easy"

    if ask_total_resistance:
        prompt = "Find the total resistance of the series circuit."
        answer = total_resistance
        unit = "ohms"
        wire_label = f"I = {format_answer_value(current)} A"
        source_label = f"{format_answer_value(source_voltage)} V"
        explanation = (
            f"In series, resistances add: R_total = R1 + R2 = "
            f"{format_answer_value(r1)} ohms + {format_answer_value(r2)} ohms = {format_answer_value(total_resistance)} ohms."
        )
    else:
        prompt = "Find the current in the series circuit."
        answer = current
        unit = "A"
        wire_label = "I = ? A"
        source_label = f"{format_answer_value(source_voltage)} V"
        explanation = (
            f"First add the resistors: R_total = {format_answer_value(r1)} ohms + {format_answer_value(r2)} ohms = "
            f"{format_answer_value(total_resistance)} ohms. Then use I = V / R_total = "
            f"{format_answer_value(source_voltage)} V / {format_answer_value(total_resistance)} ohms = {format_answer_value(current)} A."
        )

    return {
        "problem_type": "Series Current",
        "difficulty": difficulty,
        "prompt": prompt,
        "answer": answer,
        "unit": unit,
        "givens": (
            ("R1", f"{format_answer_value(r1)} ohms"),
            ("R2", f"{format_answer_value(r2)} ohms"),
            ("Battery voltage", f"{format_answer_value(source_voltage)} V"),
        ),
        "diagram": {
            "kind": "series",
            "source_label": source_label,
            "resistor_labels": [f"R1 = {format_answer_value(r1)} ohms", f"R2 = {format_answer_value(r2)} ohms"],
            "wire_label": wire_label,
        },
        "answer_label": "Total resistance" if ask_total_resistance else "Current",
        "explanation": explanation,
    }


def _build_voltage_drop_case(difficulty: str) -> dict:
    if difficulty == "Easy":
        resistance_pairs = ((2, 4), (3, 6), (4, 8), (5, 10))
        current = random.randint(1, 3)
    elif difficulty == "Medium":
        resistance_pairs = ((3, 9), (4, 12), (5, 15), (6, 18))
        current = random.choice((0.5, 1.0, 1.5, 2.0))
    else:
        resistance_pairs = ((2.5, 7.5), (4.0, 12.0), (5.0, 10.0), (6.0, 15.0))
        current = random.choice((0.6, 0.8, 1.2, 1.5, 2.4))

    r1, r2 = random.choice(resistance_pairs)
    source_voltage = (r1 + r2) * current
    target_index = random.choice((0, 1))
    target_name = f"R{target_index + 1}"
    target_resistance = (r1, r2)[target_index]
    answer = current * target_resistance

    return {
        "problem_type": "Voltage Drop",
        "difficulty": difficulty,
        "prompt": f"Find the voltage drop across {target_name}.",
        "answer": answer,
        "unit": "V",
        "givens": (
            ("Battery voltage", f"{format_answer_value(source_voltage)} V"),
            ("R1", f"{format_answer_value(r1)} ohms"),
            ("R2", f"{format_answer_value(r2)} ohms"),
        ),
        "diagram": {
            "kind": "series",
            "source_label": f"{format_answer_value(source_voltage)} V",
            "resistor_labels": [f"R1 = {format_answer_value(r1)} ohms", f"R2 = {format_answer_value(r2)} ohms"],
            "wire_label": "",
        },
        "answer_label": f"Voltage across {target_name}",
        "explanation": (
            f"First find the series current: I = V / R_total = {format_answer_value(source_voltage)} V / "
            f"{format_answer_value(r1 + r2)} ohms = {format_answer_value(current)} A. "
            f"Then use V = IR for {target_name}: {format_answer_value(current)} A x "
            f"{format_answer_value(target_resistance)} ohms = {format_answer_value(answer)} V."
        ),
    }


def build_circuit_case(problem_type: str, difficulty: str) -> dict:
    if problem_type == "Single Resistor":
        return _build_single_resistor_case(difficulty)
    if problem_type == "Series Current":
        return _build_series_current_case(difficulty)
    if problem_type == "Voltage Drop":
        return _build_voltage_drop_case(difficulty)
    raise ValueError(f"Unsupported circuit problem type: {problem_type}")
