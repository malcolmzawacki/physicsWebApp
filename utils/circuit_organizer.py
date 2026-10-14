"""Numeric organizer facts for the existing two-resistor circuit tasks."""


def circuit_plan(shared_label, shared_value, r1, r2, *, series, steps=(), component_help=None):
    if component_help is None and shared_label:
        component_help = ("The circuit current also passes through this resistor. Use V = IR to find its voltage."
                          if series else "The source voltage is also across this resistor. Use I = V/R to find its current.")
    groups = []
    if shared_label:
        groups.append({"label": "Whole circuit", "fields": [{"id": "shared", "label": shared_label, "value": shared_value}]})
    groups.extend({"label": f"R{index}", "fields": [{"id": f"R{index}", "label": f"Resistance R{index} (ohms)", "value": resistance, "help": component_help}]}
                  for index, resistance in enumerate((r1, r2), 1))
    return {"groups": groups, "steps": list(steps)}


def plan_from_case(case):
    kind = case.get("problem_type", "")
    supported = ("Series Current and Voltage", "Parallel Current and Voltage", "Series Voltage Drop",
                 "Series Equivalent Resistance", "Parallel Equivalent Resistance", "Series Total Current", "Parallel Branch Current")
    if kind not in supported:
        return None
    values = [float(value.split()[0]) for _, value in case["givens"]]
    equivalent = kind in ("Series Equivalent Resistance", "Parallel Equivalent Resistance")
    shared, r1, r2 = (None, *values) if equivalent else values
    steps = []
    if kind in ("Series Total Current", "Series Voltage Drop"):
        steps.append({"id": "Req", "label": "Equivalent resistance (ohms)", "value": r1 + r2, "help": "In series: add R1 and R2."})
    if kind == "Series Voltage Drop":
        steps.append({"id": "I", "label": "Circuit current (A)", "value": shared / (r1 + r2), "help": "Source voltage ÷ equivalent resistance. This current passes through both resistors."})
    help_text = "Use the resistance of the branch named in the question; each parallel branch has the source voltage." if kind == "Parallel Branch Current" else None
    if equivalent:
        help_text = "In series: equivalent resistance = R1 + R2." if kind.startswith("Series") else "In parallel: 1 / equivalent resistance = 1 / R1 + 1 / R2."
    if kind == "Series Total Current":
        help_text = "Combine the resistances to find the circuit's equivalent resistance."
    return circuit_plan(None if equivalent else "Circuit current (A)" if kind == "Series Current and Voltage" else "Source voltage (V)",
                        shared, r1, r2, series=kind.startswith("Series"), steps=steps, component_help=help_text)
