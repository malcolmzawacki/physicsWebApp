"""Extend thermal stage organization with constant friction over a path."""
import random
import re
from functools import wraps
from utils.thermal_organizer import thermal_payload, UnusableThermalCase, LABELS


def displayable_friction_case(method):
    @wraps(method)
    def wrapped(self, difficulty, *, variant=None):
        simple = method.__name__ in ("grav_to_kinetic_friction_distance_q", "kinetic_to_grav_friction_distance_q")
        maximum = (2 if simple else 3) if difficulty == "Easy" else (4 if simple else 5)
        variant = random.randint(0, maximum) if variant is None else variant
        for _ in range(100):
            try:
                return method(self, difficulty, variant=variant)
            except UnusableThermalCase:
                continue
        raise ValueError("Could not sample valid displayed friction/distance facts")
    return wrapped


def friction_payload(direction, values, question, units):
    def role(label):
        if "Thermal" in label: return "T"
        if "Velocity" in label: return "v"
        if "Compression" in label: return "x"
        if "Spring Constant" in label: return "k"
        if "Mass" in label: return "m"
        if "Height" in label: return "h"
        if "Force of Friction" in label: return "F"
        return "d"
    targets = [role(unit) for unit in units]
    target = targets[-1]
    values = {key: round(value, 2) for key, value in values.items()}
    if any(value <= 0 for key, value in values.items() if key not in targets and key != "T"):
        raise UnusableThermalCase("Nonpositive displayed friction fact")
    mechanical = {key: value for key, value in values.items() if key not in ("F", "d")}
    mechanical["T"] = values["F"] * values["d"]
    result = thermal_payload(direction, mechanical, "T" if target in ("F", "d") else target, question, thermal_is_calculated=True)
    plan = result["extras"]["energy_plan"]
    thermal = result["answers"][0] if target in ("F", "d") else mechanical["T"]
    if target in ("F", "d"):
        answer = thermal / values["d" if target == "F" else "F"]
        values[target] = answer
        # A ramp's traveled path cannot be shorter than its vertical change.
        if target == "d" and "h" in values and answer < values["h"]:
            raise UnusableThermalCase("Impossible ramp geometry after rounding")
    else:
        answer = result["answers"][0]
        if target == "h" and answer > values["d"]:
            raise UnusableThermalCase("Ramp height exceeds path length")
    plan["givens"].pop("T", None)
    for group in plan["groups"]:
        group["fields"] = [field for field in group["fields"] if field["id"] != "T"]
    plan["groups"] = [group for group in plan["groups"] if group["fields"]]
    extra_labels = {"F": "Friction force magnitude (N)", "d": "Distance along path (m)"}
    path_fields = [{"id": key, "label": extra_labels[key], "value": values[key]} for key in ("F", "d") if key not in targets]
    plan["groups"].append({"label": "Along the path", "fields": path_fields})
    plan["givens"].update({key: values[key] for key in ("F", "d") if key not in targets})
    thermal_step = {"id": "T", "label": "Thermal energy (J)", "value": thermal,
                    "help": "Constant friction: force magnitude × distance along the rough path." if target not in ("F", "d") else "Starting mechanical energy − ending mechanical energy. Divide by the supplied force or distance to find the other."}
    plan["steps"] = ([thermal_step] + plan["steps"]) if target not in ("F", "d") else (plan["steps"] + [thermal_step])
    plan["targets"] = targets
    plan["target"] = target
    plan["given_help"] += " Friction force means its positive magnitude and is constant over the stated path. Ramp length is measured along the slope, not vertically; any horizontal spring section is smooth."
    result["answers"] = [thermal, answer] if len(targets) == 2 else [answer]
    labels = {**LABELS, **extra_labels}
    result["units"] = [labels[key] for key in targets]
    # Some older spring prompts omitted the unit after their numeric constant.
    result["question"] = re.sub(r'(spring (?:with strength|with spring constant|of strength|has a strength of)\s+[\d.]+)(?![\d.])(?=\s+by)', r'\1 N/m', result["question"])
    return result
