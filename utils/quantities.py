"""Shared physical definitions and role-specific notation for migrated activities."""
from dataclasses import dataclass
from string import Template

@dataclass(frozen=True)
class Quantity:
    name: str
    unit: str
    dimension: str

QUANTITIES = {
    "energy": Quantity("Energy", "J", "mass*length^2/time^2"),
    "spring_constant": Quantity("Spring constant", "N/m", "mass/time^2"),
    "force": Quantity("Force", "N", "mass*length/time^2"),
    "mass": Quantity("Mass", "kg", "mass"),
    "momentum": Quantity("Momentum", "Ns", "mass*length/time"),
    "displacement": Quantity("Displacement", "m", "length"),
    "distance": Quantity("Distance", "m", "length"),
    "duration": Quantity("Time", "s", "time"),
    "velocity": Quantity("Velocity", "m/s", "length/time"),
    "speed": Quantity("Speed", "m/s", "length/time"),
    "acceleration": Quantity("Acceleration", "m/s^2", "length/time^2"),
    "wavelength": Quantity("Wavelength", "m", "length"),
    "frequency": Quantity("Frequency", "Hz", "1/time"),
    "potential_difference": Quantity("Voltage", "V", "mass*length^2/time^3/current"),
    "electric_current": Quantity("Current", "A", "current"),
    "resistance": Quantity("Resistance", "ohms", "mass*length^2/time^3/current^2"),
}

@dataclass(frozen=True)
class QuantityRole:
    quantity: str
    name: str
    symbol: str
    phase: str = ""

# Keys are local role IDs, never global physical identities.
PROFILES = {
    "kinetic_energy": {
        "E": QuantityRole("energy", "Kinetic energy", "KE"),
        "m": QuantityRole("mass", "Mass", "m"),
        "v": QuantityRole("speed", "Speed", "v"),
    },
    "elastic_energy": {
        "E": QuantityRole("energy", "Elastic potential energy", "EPE"),
        "k": QuantityRole("spring_constant", "Spring constant", "k"),
        "x": QuantityRole("distance", "Deformation", r"\Delta x"),
    },
    "gravitational_energy": {
        "E": QuantityRole("energy", "Gravitational potential energy", "GPE"),
        "m": QuantityRole("mass", "Mass", "m"),
        "g": QuantityRole("acceleration", "Gravitational acceleration", "g"),
        "h": QuantityRole("distance", "Height above reference", "h"),
    },
    "work": {
        "W": QuantityRole("energy", "Work", "W"),
        "F": QuantityRole("force", "Applied force", "F"),
        "d": QuantityRole("distance", "Distance along force", "d"),
    },
    "newtons_second_law": {
        "Fnet": QuantityRole("force", "Net force", r"\Sigma F"),
        "m": QuantityRole("mass", "Mass", "m"),
        "a": QuantityRole("acceleration", "Acceleration", "a"),
    },
    "single_resistor": {
        "V": QuantityRole("potential_difference", "Battery voltage", "V"),
        "I": QuantityRole("electric_current", "Current", "I"),
        "R": QuantityRole("resistance", "Resistance", "R"),
    },
    "wave_properties": {
        "v": QuantityRole("speed", "Wave speed", "v"),
        "wavelength": QuantityRole("wavelength", "Wavelength", r"\lambda"),
        "f": QuantityRole("frequency", "Frequency", "f"),
        "T": QuantityRole("duration", "Period", "T"),
    },
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
