from __future__ import annotations

import random
from utils.quantities import PROFILES, QUANTITIES, equation
from utils.setup_schema import make_setup
from utils.circuit_organizer import circuit_plan


PROBLEM_TYPES: tuple[str, ...] = (
    "Single Resistor",
    "Series Current and Voltage",
    "Parallel Current and Voltage",
)


CIRCUIT_MODEL_NOTES = {
    "scope": (
        "This starter activity uses ideal batteries, ideal wires, and resistors that obey Ohm's law."
    ),
    "current": (
        "In a simple series circuit, the same current passes through each resistor."
    ),
    "parallel": (
        "In parallel, each resistor has the source voltage across it."
    ),
}


CIRCUIT_EQUATION_METADATA = {
    "Single Resistor": {
        "honors": equation("single_resistor", r"${V} = ${I}${R}"),
        "conceptual": equation("single_resistor", r"${V} = ${I}${R} \quad,\quad ${I} = \frac{${V}}{${R}} \quad,\quad ${R} = \frac{${V}}{${I}}"),
    },
    "Series Current and Voltage": {
        "honors": r"I_1 = I_2 = I \quad,\quad V_1 = IR_1 \quad,\quad V_2 = IR_2",
        "conceptual": r"I_1 = I_2 = I \quad,\quad V_1 = IR_1 \quad,\quad V_2 = IR_2",
    },
    "Parallel Current and Voltage": {
        "honors": r"V_1 = V_2 = V \quad,\quad I_1 = \frac{V}{R_1} \quad,\quad I_2 = \frac{V}{R_2}",
        "conceptual": r"V_1 = V_2 = V \quad,\quad I_1 = \frac{V}{R_1} \quad,\quad I_2 = \frac{V}{R_2}",
    },
}


def format_answer_value(value: float) -> str:
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _build_single_resistor_case(difficulty: str, solve_for=None) -> dict:
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
    if solve_for is None:
        solve_for = random.choice(("Voltage", "Current", "Resistance"))
    if solve_for not in ("Voltage", "Current", "Resistance"):
        raise ValueError(f"Unsupported single-resistor target: {solve_for}")

    roles = PROFILES["single_resistor"]
    target = {"Voltage": "V", "Current": "I", "Resistance": "R"}[solve_for]
    # Normalize at the display boundary; checking and calculations use exactly
    # the same values supplied by the diagram and Givens panel.
    values = {key: float(format_answer_value(value)) for key, value in
              {"V": voltage, "I": current, "R": resistance}.items()}
    shown = {key: f"{format_answer_value(value)} {QUANTITIES[roles[key].quantity].unit}"
             for key, value in values.items()}
    diagram = {
        "kind": "single",
        "source_label": shown["V"] if target != "V" else f"? {QUANTITIES[roles['V'].quantity].unit}",
        "resistor_labels": [shown["R"] if target != "R" else f"? {QUANTITIES[roles['R'].quantity].unit}"],
        "wire_label": f"{roles['I'].symbol} = " + (shown["I"] if target != "I" else f"? {QUANTITIES[roles['I'].quantity].unit}"),
    }

    if solve_for == "Voltage":
        prompt = "Use Ohm's law to calculate the battery voltage."
        answer = values["I"] * values["R"]
        unit = QUANTITIES[roles["V"].quantity].unit
        givens = (
            (roles["R"].name, shown["R"]),
            (roles["I"].name, shown["I"]),
        )
        explanation = (
            f"Use V = IR. With I = {format_answer_value(current)} A and "
            f"R = {format_answer_value(resistance)} ohms, the voltage is {format_answer_value(voltage)} V."
        )
    elif solve_for == "Current":
        prompt = "Use Ohm's law to calculate the current in the circuit."
        answer = values["V"] / values["R"]
        unit = QUANTITIES[roles["I"].quantity].unit
        givens = (
            (roles["V"].name, shown["V"]),
            (roles["R"].name, shown["R"]),
        )
        explanation = (
            f"Use I = V / R. With V = {format_answer_value(voltage)} V and "
            f"R = {format_answer_value(resistance)} ohms, the current is {format_answer_value(current)} A."
        )
    else:
        prompt = "Use Ohm's law to calculate the resistance of the resistor."
        answer = values["V"] / values["I"]
        unit = QUANTITIES[roles["R"].quantity].unit
        givens = (
            (roles["V"].name, shown["V"]),
            (roles["I"].name, shown["I"]),
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
        "setup": make_setup("single_resistor", values, set(values) - {target}, [target]),
    }


def _build_relationship_case(problem_type: str, difficulty: str) -> dict:
    if difficulty == "Easy":
        r1, r2 = random.choice(((2, 4), (3, 6), (4, 8), (5, 10)))
        current = random.randint(1, 3)
    elif difficulty == "Medium":
        r1, r2 = random.choice(((3, 9), (4, 12), (5, 15), (6, 18)))
        current = random.choice((0.5, 1.0, 1.5, 2.0))
    else:
        r1, r2 = random.choice(((2.5, 7.5), (4.0, 12.0), (5.0, 10.0), (6.0, 15.0)))
        current = random.choice((0.6, 0.8, 1.2, 1.5, 2.4))
    fmt = format_answer_value
    diagram = {
        "kind": "series", "source_label": "",
        "resistor_labels": [f"R1 = {fmt(r1)} ohms", f"R2 = {fmt(r2)} ohms"],
        "wire_label": "",
    }
    resistances = (("R1", f"{fmt(r1)} ohms"), ("R2", f"{fmt(r2)} ohms"))
    if problem_type == "Series Current and Voltage":
        answers, unit = [current * r1, current * r2], "V"
        labels = ["Voltage across R1", "Voltage across R2"]
        prompt = "The shared series current is given. Find the voltage across each resistor."
        relationship = "One path: the given current passes through both R1 and R2. Use each resistor's own resistance to find its voltage."
        givens = (("Shared current", f"{fmt(current)} A"), *resistances)
        diagram["wire_label"] = f"I = {fmt(current)} A"
        explanation = (
            f"The same {fmt(current)} A passes through each resistor. "
            f"V1 = I x R1 = {fmt(current)} A x {fmt(r1)} ohms = {fmt(answers[0])} V. "
            f"V2 = I x R2 = {fmt(current)} A x {fmt(r2)} ohms = {fmt(answers[1])} V. "
            "With the same current, the larger resistor has the larger voltage drop. "
            "No equivalent resistance or source-voltage calculation is needed."
        )
    else:
        if difficulty == "Easy":
            source = random.choice((6, 12, 18))
        elif difficulty == "Medium":
            source = random.choice((9, 12, 15, 18, 20))
        else:
            source = random.choice((7.5, 12, 16, 18, 24))
        answers, unit = [source / r1, source / r2], "A"
        labels = ["Current through R1", "Current through R2"]
        diagram.update(kind="parallel", source_label=f"{fmt(source)} V")
        prompt = "The source voltage is given. Find the current through each parallel resistor."
        relationship = "Both branches span the source terminals: each resistor has the full source voltage. Use each branch's own resistance to find its current."
        givens = (("Source voltage", f"{fmt(source)} V"), *resistances)
        explanation = (
            f"Each resistor has the full {fmt(source)} V across it. "
            f"I1 = V / R1 = {fmt(source)} V / {fmt(r1)} ohms = {fmt(answers[0])} A. "
            f"I2 = V / R2 = {fmt(source)} V / {fmt(r2)} ohms = {fmt(answers[1])} A. "
            "With the same voltage, the larger resistor draws less current. "
            "No equivalent resistance or total-current calculation is needed."
        )
    return dict(problem_type=problem_type, difficulty=difficulty, prompt=prompt,
                answers=answers, answer_labels=labels, unit=unit, givens=givens,
                diagram=diagram, relationship=relationship, explanation=explanation,
                organizer=circuit_plan("Circuit current (A)" if problem_type == "Series Current and Voltage" else "Source voltage (V)",
                                       current if problem_type == "Series Current and Voltage" else source,
                                       r1, r2, series=problem_type == "Series Current and Voltage"))


def build_circuit_case(problem_type: str, difficulty: str, solve_for=None) -> dict:
    if solve_for is not None and problem_type != "Single Resistor":
        raise ValueError("Explicit targets are only supported for Single Resistor")
    if problem_type == "Single Resistor":
        return _build_single_resistor_case(difficulty, solve_for)
    if problem_type in PROBLEM_TYPES:
        return _build_relationship_case(problem_type, difficulty)
    raise ValueError(f"Unsupported circuit problem type: {problem_type}")
