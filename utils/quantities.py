"""Shared physical definitions and role-specific notation for migrated activities."""
from dataclasses import dataclass
from string import Template

@dataclass(frozen=True)
class Quantity:
    name: str
    unit: str
    dimension: str

QUANTITIES = {
    "mass": Quantity("Mass", "kg", "mass"),
    "momentum": Quantity("Momentum", "Ns", "mass*length/time"),
    "displacement": Quantity("Displacement", "m", "length"),
    "distance": Quantity("Distance", "m", "length"),
    "duration": Quantity("Time", "s", "time"),
    "velocity": Quantity("Velocity", "m/s", "length/time"),
    "speed": Quantity("Speed", "m/s", "length/time"),
    "acceleration": Quantity("Acceleration", "m/s^2", "length/time^2"),
}

@dataclass(frozen=True)
class QuantityRole:
    quantity: str
    name: str
    symbol: str
    phase: str = ""

# Keys are local role IDs, never global physical identities.
PROFILES = {
    "momentum": {
        "p": QuantityRole("momentum", "Momentum", "p"),
        "m": QuantityRole("mass", "Mass", "m"),
        "v": QuantityRole("velocity", "Velocity", "v"),
    },
    "linear_motion": {
        "x": QuantityRole("displacement", "Displacement", "x"),
        "t": QuantityRole("duration", "Time", "t"),
        "vi": QuantityRole("velocity", "Initial velocity", "v_i", "initial"),
        "vf": QuantityRole("velocity", "Final velocity", "v_f", "final"),
        "a": QuantityRole("acceleration", "Acceleration", "a"),
    },
    "constant_speed": {
        "d": QuantityRole("distance", "Distance", "d"),
        "t": QuantityRole("duration", "Time", "t"),
        "v": QuantityRole("speed", "Speed", "v"),
    },
}


def equation(profile, template):
    """Substitute explicit ${role} tokens; never infer meaning from LaTeX."""
    return Template(template).substitute({key: role.symbol for key, role in PROFILES[profile].items()})
