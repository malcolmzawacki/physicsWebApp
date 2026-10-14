"""Thermal energy balances using the facts printed in the question."""
import math
import random
from functools import wraps

STATES = {
    "grav_to_kin": ("gravity", "kinetic", "Start: ramp top", "End: ramp bottom"),
    "kin_to_grav": ("kinetic", "gravity", "Start: ramp bottom", "End: stopped on ramp"),
    "grav_to_elastic": ("gravity", "spring", "Start: ramp top", "End: spring compressed"),
    "elastic_to_grav": ("spring", "gravity", "Start: spring compressed", "End: stopped on ramp"),
    "kinetic_to_elastic": ("kinetic", "spring", "Start: moving", "End: spring compressed"),
    "elastic_to_kinetic": ("spring", "kinetic", "Start: spring compressed", "End: moving"),
}
LABELS = {"m": "Mass (kg)", "h": "Vertical height (m)", "v": "Speed (m/s)",
          "k": "Spring constant (N/m)", "x": "Compression (m)", "T": "Thermal energy (J)"}
ROLES = {"gravity": ("h",), "kinetic": ("v",), "spring": ("k", "x")}
NAMES = {"gravity": "gravitational potential energy", "kinetic": "kinetic energy", "spring": "elastic potential energy"}
FORMULAS = {"gravity": "mass × g × vertical height", "kinetic": "½ mass × speed²", "spring": "½ spring constant × compression²"}


class UnusableThermalCase(ValueError):
    pass


def displayable_case(method):
    """Resample the same target if rounded facts would describe an impossible case."""
    @wraps(method)
    def wrapped(*args, **kwargs):
        # Keep a randomly chosen variant stable across a precision retry.
        kwargs = dict(kwargs)
        if kwargs.get("variant") is None:
            kwargs["variant"] = random.randint(0, 2 if method.__name__ in ("grav_to_kin_thermal_q", "kin_to_grav_thermal_q") else 4)
        for _ in range(100):
            try:
                return method(*args, **kwargs)
            except UnusableThermalCase:
                continue
        raise ValueError("Could not sample a valid displayed thermal-energy problem")
    return wrapped


def energy(kind, values):
    if kind == "gravity":
        return values["m"] * 10 * values["h"]
    if kind == "kinetic":
        return .5 * values["m"] * values["v"]**2
    return .5 * values["k"] * values["x"]**2


def thermal_payload(direction, values, target, question, *, thermal_is_calculated=False):
    values = {key: value if key == "T" and thermal_is_calculated else round(value, 2) for key, value in values.items()}
    givens = {key: value for key, value in values.items() if key != target}
    if any(value <= 0 or not math.isfinite(value) for value in givens.values()):
        raise UnusableThermalCase("Nonpositive displayed fact")
    initial, final, initial_label, final_label = STATES[direction]
    if target == "T":
        answer = energy(initial, values) - energy(final, values)
    elif target == "m":
        def mass_coefficient(kind):
            return 10*values["h"] if kind == "gravity" else .5*values["v"]**2 if kind == "kinetic" else 0
        spring_difference = (.5*values["k"]*values["x"]**2 if initial == "spring" else 0) - (.5*values["k"]*values["x"]**2 if final == "spring" else 0)
        answer = (values["T"] - spring_difference) / (mass_coefficient(initial) - mass_coefficient(final))
    else:
        unknown_initial = target in ROLES[initial]
        kind = initial if unknown_initial else final
        other = final if unknown_initial else initial
        desired = energy(other, values) + values["T"] if unknown_initial else energy(other, values) - values["T"]
        if desired <= 0:
            raise UnusableThermalCase("No positive residual energy")
        answer = (desired/(10*values["m"]) if target == "h" else
                  math.sqrt(2*desired/values["m"]) if target == "v" else
                  2*desired/values["x"]**2 if target == "k" else math.sqrt(2*desired/values["k"]))
    if not math.isfinite(answer) or answer <= 0:
        raise UnusableThermalCase("Rounded facts imply nonpositive answer")
    values[target] = answer
    groups = []
    for label, keys in (("Shared", ("m", "T")), (initial_label, ROLES[initial]), (final_label, ROLES[final])):
        fields = [{"id": key, "label": LABELS[key], "value": values[key]} for key in keys if key in givens]
        if fields:
            groups.append({"label": label, "fields": fields})
    steps = []
    for key, kind, other, sign in (("Ei", initial, final, "+"), ("Ef", final, initial, "−")):
        directly_known = all(role in givens for role in ROLES[kind]) and (kind == "spring" or "m" in givens)
        hint = f"Use {FORMULAS[kind]}." if directly_known else f"Use the {'ending' if key == 'Ei' else 'starting'} mechanical energy {sign} thermal energy."
        steps.append({"id": key, "label": f"{'Starting' if key == 'Ei' else 'Ending'} {NAMES[kind]} (J)", "value": energy(kind, values), "help": hint})
    question = question.replace("Work done by Friction", "Thermal energy").replace("velocity", "speed").replace("Velocity", "Speed").replace("was lost", "lost")
    question = question.replace("spring of strength", "spring with spring constant").replace("has a strength of", "has a spring constant of").replace("with a strength of", "with a spring constant of")
    question = question.replace("How strong is the spring?", "What is the spring constant?").replace("how strong is the spring?", "what is the spring constant?")
    if direction == "kin_to_grav":
        question = question.replace("slides up a ramp, reaching a height", "slides up a ramp and stops at a height")
        question = question.replace("meters up a ramp.", "meters vertically up a ramp before stopping.")
    if direction == "elastic_to_grav":
        question = question.replace("slides up a ramp to a height", "slides up a ramp and stops at a height").replace("slides up to the top", "slides up and stops at the top").replace("reaches a height", "comes to rest at a height")
        question = question.replace("launched up a ramp to a height", "launched up a ramp and comes to rest at a height")
    if direction == "kinetic_to_elastic":
        question = question.replace("compressing the spring at the bottom by", "compressing the spring by")
    plan = {"groups": groups, "steps": steps, "target": target, "givens": givens, "direction": direction,
            "given_help": "Use g = 10 m/s². Ramp height is vertical. Springs are ideal and horizontal, at the ramp's top or bottom where applicable. Thermal energy is the positive mechanical energy lost; work done by friction is its negative. Moving states have relaxed springs; maximum height and maximum compression are rest states."}
    return {"question": question, "answers": [answer], "units": [LABELS[target]], "extras": {"energy_plan": plan}}
